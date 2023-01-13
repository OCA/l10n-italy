# Copyright (C) 2012 Andrea Cometa.
# Email: info@andreacometa.it
# Web site: http://www.andreacometa.it
# Copyright (C) 2012 Associazione OpenERP Italia
# (<http://www.odoo-italia.org>).
# Copyright (C) 2012-2017 Lorenzo Battistini - Agile Business Group
# Copyright 2023 Simone Rubino - Aion Tech
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
        list_ids = []
        for line in self.env["account.move.line"].search(
            [
                "&",
                "|",
                ("riba", "=", "True"),
                ("past_due_invoice_ids", "!=", False),
                ("account_id.account_type", "=", "asset_receivable"),
            ],
            order="date_maturity asc, price_total asc",
        ):
            if (
                self.currency_id.compare_amounts(
                    line.amount_residual,
                    self.presentation_amount,
                )
                > 0
            ):
                break
            self.presentation_amount -= line.amount_residual
            list_ids.append(line.id)
        res = self.env["ir.actions.act_window"]._for_xml_id(
            "l10n_it_riba.action_riba_to_issue"
        )
        res["domain"] = [("id", "in", list_ids)]
        return res
