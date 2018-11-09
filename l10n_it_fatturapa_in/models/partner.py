# -*- coding: utf-8 -*-

from openerp.osv import fields, orm


class Partner(orm.Model):
    _inherit = 'res.partner'


    _columns = {
        'e_invoice_default_product_id': fields.many2one(
            'product.product',
            string='Default product electronic invoice',
            help="Used by electronic invoice XML import. "
             "If filled, generated invoice lines will use this product, when "
             "no other possible product is found."
             ),
        
    'e_invoice_detail_level': fields.selection([
        ('0', 'Minimo'),
        # ('1', 'Aliquote'),
        ('2', 'Massimo'),
        ], string="Livello di dettaglio Fatture elettroniche passive",
        help="Livello minimo: La fattura passiva viene creata senza righe; "
             "sara' l'utente a doverle creare in base a quanto indicato dal "
             "fornitore nella fattura elettronica\n"
             # "Livello Aliquote: viene creata una riga fattura per ogni "
             # "aliquota presente nella fattura elettronica\n"
             "Livello Massimo: tutte le righe presenti nella fattura "
             "elettronica vengono create come righe della fattura passiva",
        required=True
        ),
        
        }
    
    _defaults = {
        'e_invoice_detail_level': '2',
        }
