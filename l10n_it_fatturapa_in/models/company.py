# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    dati_bollo_product_id = fields.Many2one(
        'product.product', 'Stamp Data Product',
        help="Product used to model DatiBollo XML element on bills."
        )
    cassa_previdenziale_product_id = fields.Many2one(
        'product.product', 'Welfare Fund Data Product',
        help="Product used to model DatiCassaPrevidenziale XML element "
             "on bills."
        )
    sconto_maggiorazione_product_id = fields.Many2one(
        'product.product', 'Discount Supplement Product',
        help="Product used to model ScontoMaggiorazione XML element on bills."
        )


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    dati_bollo_product_id = fields.Many2one(
        related='company_id.dati_bollo_product_id',
        string="Stamp Data Product",
        help="Product used to model DatiBollo XML element on bills."
        )
    cassa_previdenziale_product_id = fields.Many2one(
        related='company_id.cassa_previdenziale_product_id',
        string="Welfare Fund Data Product",
        help="Product used to model DatiCassaPrevidenziale XML element "
             "on bills."
        )
    sconto_maggiorazione_product_id = fields.Many2one(
        related='company_id.sconto_maggiorazione_product_id',
        string="Discount Supplement Product",
        help="Product used to model ScontoMaggiorazione XML element on bills."
        )

    @api.onchange('company_id')
    def onchange_company_id(self):
        res = super(AccountConfigSettings, self).onchange_company_id()
        if self.company_id:
            company = self.company_id
            self.dati_bollo_product_id = (
                company.dati_bollo_product_id and
                company.dati_bollo_product_id.id or False
                )
            self.cassa_previdenziale_product_id = (
                company.cassa_previdenziale_product_id and
                company.cassa_previdenziale_product_id.id or False
                )
            self.sconto_maggiorazione_product_id = (
                company.sconto_maggiorazione_product_id and
                company.sconto_maggiorazione_product_id.id or False
                )
        else:
            self.dati_bollo_product_id = False
            self.cassa_previdenziale_product_id = False
            self.sconto_maggiorazione_product_id = False
        return res
