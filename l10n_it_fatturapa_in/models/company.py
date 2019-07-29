# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    cassa_previdenziale_product_id = fields.Many2one(
        'product.product', 'Welfare Fund Data Product',
        help="Product used to model DatiCassaPrevidenziale XML element "
             "on bills."
    )
    sconto_maggiorazione_product_id = fields.Many2one(
        'product.product', 'Discount Supplement Product',
        help="Product used to model ScontoMaggiorazione XML element on bills."
        )
    arrotondamenti_attivi_account_id = fields.Many2one(
        'account.account', 'Active Rounding Account',
        domain=[('deprecated', '=', False)],
        help="Account used for active rounding amount on bills."
        )
    arrotondamenti_passivi_account_id = fields.Many2one(
        'account.account', 'Passive Rounding Account',
        domain=[('deprecated', '=', False)],
        help="Account used for passive rounding amount on bills."
        )
    arrotondamenti_tax_id = fields.Many2one(
        'account.tax', 'Rounding Tax',
        domain=[('type_tax_use', '=', 'purchase'), ('amount', '=', 0.0)],
        help="Tax used for rounding amount on bills."
        )


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    cassa_previdenziale_product_id = fields.Many2one(
        related='company_id.cassa_previdenziale_product_id',
    )
    sconto_maggiorazione_product_id = fields.Many2one(
        related='company_id.sconto_maggiorazione_product_id',
    )
    arrotondamenti_attivi_account_id = fields.Many2one(
        related='company_id.arrotondamenti_attivi_account_id',
    )
    arrotondamenti_passivi_account_id = fields.Many2one(
        related='company_id.arrotondamenti_passivi_account_id',
    )
    arrotondamenti_tax_id = fields.Many2one(
        related='company_id.arrotondamenti_tax_id',
    )
