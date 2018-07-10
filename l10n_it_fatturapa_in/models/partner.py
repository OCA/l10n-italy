# -*- coding: utf-8 -*-

from odoo import models, fields


class Partner(models.Model):
    _inherit = 'res.partner'

    e_invoice_default_product_id = fields.Many2one(
        comodel_name='product.product',
        string='Default product electronic invoice',
        help="Used by electronic invoice XML import. "
             "If filled, generated invoice lines will use this product, when "
             "no other possible product is found."
    )
    e_invoice_detail_level = fields.Selection([
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
        default='2', required=True
    )
