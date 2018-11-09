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

        # TODO: check model relation
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
