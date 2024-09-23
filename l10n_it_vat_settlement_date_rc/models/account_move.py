# Copyright (c) 2021 Marco Colombo (https://github/TheMule71)
# Copyright 2024 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def rc_inv_vals(self, partner, rc_type, lines, currency):
        invoice_values = super().rc_inv_vals(partner, rc_type, lines, currency)
        invoice_values["l10n_it_vat_settlement_date"] = self.l10n_it_vat_settlement_date
        return invoice_values
