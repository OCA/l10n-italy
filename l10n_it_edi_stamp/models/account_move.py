#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountMove (models.Model):
    _inherit = "account.move"

    l10n_it_stamp_duty = fields.Float(
        compute="_compute_l10n_it_stamp_duty",
        store=True,
    )

    @api.depends(
        "l10n_it_account_stamp_is_tax_stamp_applied",
        "company_id.l10n_it_account_stamp_tax_stamp_product_id.list_price",
    )
    def _compute_l10n_it_stamp_duty(self):
        for invoice in self:
            if invoice.state != "draft":
                continue
            elif invoice.l10n_it_account_stamp_is_tax_stamp_applied:
                stamp_duty_amount = invoice.company_id.l10n_it_account_stamp_tax_stamp_product_id.list_price
            else:
                stamp_duty_amount = 0
            invoice.l10n_it_stamp_duty = stamp_duty_amount
