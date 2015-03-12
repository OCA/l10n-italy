# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Davide Corio <davide.corio@lsweb.it>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, orm


class fatturapa_document_type(orm.Model):
    _name = "fatturapa.document_type"
    _description = 'FatturaPA Document Type'

    _columns = {
        'name': fields.char('Description', size=128),
        'code': fields.char('Code', size=4),
    }


class fatturapa_payment_term(orm.Model):
    _name = "fatturapa.payment_term"
    _description = 'FatturaPA Payment Term'
    _rec_name = 'code'

    _columns = {
        'name': fields.char('Description', size=128),
        'code': fields.char('Code', size=4),
    }


class fatturapa_payment_method(orm.Model):
    _name = "fatturapa.payment_method"
    _description = 'FatturaPA Payment Method'
    _rec_name = 'code'

    _columns = {
        'name': fields.char('Description', size=128),
        'code': fields.char('Code', size=4),
    }


class fatturapa_fiscal_position(orm.Model):
    _name = "fatturapa.fiscal_position"
    _description = 'FatturaPA Fiscal Position'

    _columns = {
        'name': fields.char('Description', size=128),
        'code': fields.char('Code', size=4),
    }


class fatturapa_format(orm.Model):
    # TODO check possible formats
    _name = "fatturapa.format"
    _description = 'FatturaPA Format'

    _columns = {
        'name': fields.char('Description', size=128),
        'code': fields.char('Code', size=5),
    }


class fatturapa_related_document_type(orm.Model):
    _name = 'fatturapa.related_document_type'
    _description = 'FatturaPA Related Document Type'

    _columns = {
        'type': fields.selection([('order', 'Order'),
                                  ('contract', 'Contract'),
                                  ('agreement', 'Agreement'),
                                  ('reception', 'Reception'),
                                  ('invoice', 'Related Invoice')],
                                 'Document Type', required=True),
        'name': fields.char('DocumentID', size=128, required=True),
        'lineRef': fields.integer('LineRef'),
        'invoice_line_id': fields.many2one('account.invoice.line',
                                           'Related Invoice Line',
                                           ondelete='cascade',
                                           select=True,
                                           required=True),
        'date': fields.date('Date'),
        'numitem': fields.integer('NumItem'),
        'code': fields.char('Order Agreement Code', size=64),
        'cig': fields.char('CIG Code', size=64),
        'cup': fields.char('CUP Code', size=64),
    }

    def create(self, cr, uid, vals, context=None):
        if not context:
            context = {}
        line_obj = self.pool.get('account.invoice.line')
        line = line_obj.browse(cr, uid,
                               vals['invoice_line_id'],
                               context=context)
        vals['lineRef'] = line.sequence
        return super(fatturapa_related_document_type, self).\
            create(cr, uid, vals, context)


class account_payment_term(orm.Model):
    _inherit = 'account.payment.term'

    _columns = {
        'fatturapa_pt_id': fields.many2one(
            'fatturapa.payment_term', string="FatturaPA Payment Term"),
        'fatturapa_pm_id': fields.many2one(
            'fatturapa.payment_method', string="FatturaPA Payment Method"),
    }


class account_invoice_line(orm.Model):
    _inherit = "account.invoice.line"

    _columns = {
        'related_documents': fields.one2many('fatturapa.related_document_type',
                                             'invoice_line_id',
                                             'Related Documents Type'),
    }
