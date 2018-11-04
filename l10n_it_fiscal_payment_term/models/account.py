# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio <davide.corio@abstract.it>
# Copyright 2018 Andrea Cometa - Apulia Software
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.osv import fields, orm


class FatturapaPaymentTerm(orm.Model):
    # _position = ['2.4.1']
    _name = "fatturapa.payment_term"
    _description = 'Fiscal Payment Term'

    _columns = {
        'name': fields.char(string="Description", size=128),
        'code': fields.char(string="Code", size=4)
    }


class FatturapaPaymentMethod(orm.Model):
    # _position = ['2.4.2.2']
    _name = "fatturapa.payment_method"
    _description = 'Fiscal Payment Method'

    _columns = {
        'name': fields.char(string="Description", size=128),
        'code': fields.char(string="Code", size=4)
    }


#  used in fatturaPa export
class AccountPaymentTerm(orm.Model):
    # _position = ['2.4.2.2']
    _inherit = 'account.payment.term'

    _columns = {
        'fatturapa_pt_id': fields.many2one(
            'fatturapa.payment_term', string="Fiscal Payment Term"),
        'fatturapa_pm_id': fields.many2one(
            'fatturapa.payment_method', string="Fiscal Payment Method")
    }
