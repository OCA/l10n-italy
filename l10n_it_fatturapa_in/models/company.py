# -*- coding: utf-8 -*-

from openerp.osv import fields, orm, osv


class ResCompany(orm.Model):
    _inherit = 'res.company'

    _columns = {
        'dati_bollo_product_id': fields.many2one(
            'product.product', 'Product for Dati Bollo',
            help='Prodotto da utilizzare nelle fatture passive quando nell\'XML '
            'viene valorizzato l\'elemento DatiBollo'
            ),
        'cassa_previdenziale_product_id': fields.many2one(
            'product.product', 'Product for Dati Cassa Previdenziale',
            help='Prodotto da utilizzare nelle fatture passive quando nell\'XML '
            'viene valorizzato l\'elemento DatiCassaPrevidenziale'
            ),
        'sconto_maggiorazione_product_id': fields.many2one(
            'product.product', 'Product for Sconto Maggiorazione',
            help='Prodotto da utilizzare nelle fatture passive quando nell\'XML '
            'viene valorizzato l\'elemento ScontoMaggiorazione'
            ),
        }


class AccountConfigSettings(osv.TransientModel):
    _inherit = 'account.config.settings'

    _columns = {

        'dati_bollo_product_id': fields.related(
            'company_id', 'dati_bollo_product_id', type='many2one',
            relation='product.product', string='Product for Dati Bollo',
            help='Prodotto da utilizzare nelle fatture passive quando nell\'XML '
             'viene valorizzato l\'elemento DatiBollo'),
        'cassa_previdenziale_product_id': fields.related(
            'company_id', 'cassa_previdenziale_product_id', type='many2one',
            relation='product.product', string='Product for Dati Bollo',
            help='Prodotto da utilizzare nelle fatture passive quando nell\'XML '
             'viene valorizzato l\'elemento DatiCassaPrevidenziale'),
        'sconto_maggiorazione_product_id': fields.related(
            'company_id', 'cassa_previdenziale_product_id', type='many2one',
            relation='product.product', string='Product for Sconto Maggiorazione',
            help='Prodotto da utilizzare nelle fatture passive quando nell\'XML '
             'viene valorizzato l\'elemento ScontoMaggiorazione'),
    
    }

    def onchange_company_id(self, cr, uid, ids, company_id, context=None):
        res = super(AccountConfigSettings, self).onchange_company_id(cr, uid, ids, company_id, context)
        company_id = self.pool.get('res.company').browse(cr, uid, company_id)
        if company_id:
            res['value']['dati_bollo_product_id'] = (
                company_id.dati_bollo_product_id and
                company_id.dati_bollo_product_id.id or False
                )
            res['value']['cassa_previdenziale_product_id'] = (
                company_id.cassa_previdenziale_product_id and
                company_id.cassa_previdenziale_product_id.id or False
                )
            res['value']['sconto_maggiorazione_product_id'] = (
                company_id.sconto_maggiorazione_product_id and
                company_id.sconto_maggiorazione_product_id.id or False
                )
        else:
            res['value']['dati_bollo_product_id'] = False
            res['value']['cassa_previdenziale_product_id'] = False
            res['value']['sconto_maggiorazione_product_id'] = False
        return res
