# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    dati_bollo_product_id = fields.Many2one(
        'product.product', 'Product for Dati Bollo',
        help='Prodotto da utilizzare nelle fatture passive quando nell\'XML '
             'viene valorizzato l\'elemento DatiBollo'
        )
    cassa_previdenziale_product_id = fields.Many2one(
        'product.product', 'Product for Dati Cassa Previdenziale',
        help='Prodotto da utilizzare nelle fatture passive quando nell\'XML '
             'viene valorizzato l\'elemento DatiCassaPrevidenziale'
        )
    sconto_maggiorazione_product_id = fields.Many2one(
        'product.product', 'Product for Sconto Maggiorazione',
        help='Prodotto da utilizzare nelle fatture passive quando nell\'XML '
             'viene valorizzato l\'elemento ScontoMaggiorazione'
        )


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    dati_bollo_product_id = fields.Many2one(
        related='company_id.dati_bollo_product_id',
        string="Product for Dati Bollo",
        help='Prodotto da utilizzare nelle fatture passive quando nell\'XML '
             'viene valorizzato l\'elemento DatiBollo'
        )
    cassa_previdenziale_product_id = fields.Many2one(
        related='company_id.cassa_previdenziale_product_id',
        string="Product for Dati Cassa Previdenziale",
        help='Prodotto da utilizzare nelle fatture passive quando nell\'XML '
             'viene valorizzato l\'elemento DatiCassaPrevidenziale'
        )
    sconto_maggiorazione_product_id = fields.Many2one(
        related='company_id.sconto_maggiorazione_product_id',
        string="Product for Sconto Maggiorazione",
        help='Prodotto da utilizzare nelle fatture passive quando nell\'XML '
             'viene valorizzato l\'elemento ScontoMaggiorazione'
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
