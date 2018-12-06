# -*- coding: utf-8 -*-

from openerp import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'
    sconto_maggiorazione_product_id = fields.Many2one(
        'product.product', 'Product for Sconto Maggiorazione',
        help='Prodotto da utilizzare nelle fatture passive quando nell\'XML '
             'viene valorizzato l\'elemento ScontoMaggiorazione'
        )


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'
    sconto_maggiorazione_product_id = fields.Many2one(
        related='company_id.sconto_maggiorazione_product_id',
        string="Product for Sconto Maggiorazione",
        help='Prodotto da utilizzare nelle fatture passive quando nell\'XML '
             'viene valorizzato l\'elemento ScontoMaggiorazione'
        )

    @api.v7
    def onchange_company_id(self, cr, uid, ids, company_id, context=None):
        res = super(AccountConfigSettings, self).onchange_company_id(
            cr, uid, ids, company_id, context=context)
        if company_id:
            company = self.pool.get('res.company').browse(
                cr, uid, company_id, context=context)
            res['value'].update({
                'sconto_maggiorazione_product_id': (
                    company.sconto_maggiorazione_product_id and
                    company.sconto_maggiorazione_product_id.id or False
                    ),
            })
        else:
            res['value'].update({
                'sconto_maggiorazione_product_id': False,
            })
        return res
