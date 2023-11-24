# Copyright (C) 2012 Andrea Cometa.
# Email: info@andreacometa.it
# Web site: http://www.andreacometa.it
# Copyright (C) 2012 Associazione OpenERP Italia
# (<http://www.odoo-italia.org>).
# Copyright (C) 2012-2017 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PresentationRibaIssue(models.TransientModel):
    _name = "presentation.riba.issue"
    _description = "Presentation Riba Issue"
    currency_id = fields.Many2one(
        "res.currency", default=lambda self: self.env.company.currency_id
    )
    presentation_amount = fields.Monetary(currency_field="currency_id")

    def action_presentation_riba(self):
        active_ids = self.env.context.get("active_ids")
        move_lines = (
            self.env["account.move.line"]
            .browse(active_ids)
            .sorted(key=lambda r: (r.date_maturity, r.price_total))
        )
        if not move_lines:
            move_lines = self.env["account.move.line"].search(
                [
                    "&",
                    "|",
                    ("riba", "=", "True"),
                    ("unsolved_invoice_ids", "!=", False),
                    ("account_id.internal_type", "=", "receivable"),
                ],
                order="date_maturity asc, price_total asc",
            )
        list_ids = []
        for line in move_lines:
            if (
                self.currency_id.compare_amounts(
                    line.amount_residual,
                    self.presentation_amount,
                )
                > 0
            ):
                continue
            self.presentation_amount -= line.amount_residual
            list_ids.append(line.id)
        res = self.env["ir.actions.act_window"]._for_xml_id(
            "l10n_it_ricevute_bancarie.action_riba_da_emettere"
        )
        res["domain"] = [("id", "in", list_ids)]
        return res
