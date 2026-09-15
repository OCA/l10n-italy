# Copyright (c) 2021 Marco Colombo (https://github/TheMule71)
# Copyright 2024 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    l10n_it_vat_settlement_date = fields.Date(
        string="VAT Settlement Date",
        compute="_compute_l10n_it_vat_settlement_date",
        index=True,
        store=True,
        copy=False,
        readonly=False,
    )

    @api.depends(
        "move_id.l10n_it_vat_settlement_date",
    )
    def _compute_l10n_it_vat_settlement_date(self):
        for line in self:
            move = line.move_id
            line.l10n_it_vat_settlement_date = move.l10n_it_vat_settlement_date
