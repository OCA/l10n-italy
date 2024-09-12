# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_it_account_stamp_tax_stamp_product_id = fields.Many2one(
        comodel_name="product.product",
        string="Tax Stamp Product",
        help="Product used as Tax Stamp in customer invoices.",
    )


class AccountConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    l10n_it_account_stamp_tax_stamp_product_id = fields.Many2one(
        related="company_id.l10n_it_account_stamp_tax_stamp_product_id",
        string="Tax Stamp Product",
        help="Product used as Tax Stamp in customer invoices.",
        readonly=False,
    )
