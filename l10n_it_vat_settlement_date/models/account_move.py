# Copyright (c) 2021 Marco Colombo (https://github/TheMule71)
# Copyright 2024 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    l10n_it_vat_settlement_date = fields.Date(
        string="VAT Settlement Date",
        compute="_compute_l10n_it_vat_settlement_date",
        store=True,
        readonly=False,
    )

    @api.depends(
        "date",
        "invoice_date",
    )
    def _compute_l10n_it_vat_settlement_date(self):
        for move in self:
            settlement_date = (
                move.date or move.invoice_date or fields.Date.context_today(move)
            )
            move.l10n_it_vat_settlement_date = settlement_date
