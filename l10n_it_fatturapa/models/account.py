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
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, orm

RELATED_DOCUMENT_TYPES = {
    'order': 'DatiOrdineAcquisto',
    'contract': 'DatiContratto',
    'agreement': 'DatiConvenzione',
    'reception': 'DatiRicezione',
    'invoice': 'DatiFattureCollegate',
}


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


class fatturapa_stamp_tax(orm.Model):
    # TODO check possible formats
    _name = "fatturapa.stamp.tax"
    _description = 'FatturaPA Virtual stamp Tax'

    _columns = {
        'virtual_stamp': fields.boolean('Virtual Stamp'),
        'stamp_amount': fields.float('Stamp Amount'),
    }

class welfare_fund_type(orm.Model):
    _name = "welfare.fund.type"
    _description = 'welfare fund type'

    _columns = {
        'name': fields.char('name'),
        'description': fields.char('description'),
    }

class welfare_fund_data_line(orm.Model):
    # TODO add Natura 2.1.1.7.7
    _name = "welfare.fund.data.line"
    _description = 'FatturaPA Virtual stamp Tax'

    _columns = {
        'fund.type': fields.many2one(
            'welfare.fund.type', string="Welfare Fund Type"),
        'welfare_rate_tax': fields.float('Welfare Rate tax'),
        'welfare_amount_tax': fields.float('Welfare Amount tax'),
        'welfare_taxable': fields.float('Welfare Taxable'),
        'subjected_withholding': fields.char(
            'Subjected at Withholding', size=2),
        'pa_line_code': fields.char('PA Code for this record', size=20),
    }



class fatturapa_related_document_type(orm.Model):
    _name = 'fatturapa.related_document_type'
    _description = 'FatturaPA Related Document Type'

    _columns = {
        'type': fields.selection(
            [
                ('order', 'Order'),
                ('contract', 'Contract'),
                ('agreement', 'Agreement'),
                ('reception', 'Reception'),
                ('invoice', 'Related Invoice')
            ],
            'Document Type', required=True
        ),
        'name': fields.char('DocumentID', size=20, required=True),
        'lineRef': fields.integer('LineRef'),
        'invoice_line_id': fields.many2one(
            'account.invoice.line', 'Related Invoice Line',
            ondelete='cascade', select=True),
        'invoice_id': fields.many2one(
            'account.invoice', 'Related Invoice',
            ondelete='cascade', select=True),
        'date': fields.date('Date'),
        'numitem': fields.char('NumItem', size=20),
        'code': fields.char('Order Agreement Code', size=100),
        'cig': fields.char('CIG Code', size=14),
        'cup': fields.char('CUP Code', size=14),
    }

    def create(self, cr, uid, vals, context=None):
        if not context:
            context = {}
        if vals.get('invoice_line_id'):
            line_obj = self.pool.get('account.invoice.line')
            line = line_obj.browse(
                cr, uid, vals['invoice_line_id'], context=context)
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


class account_invoice(orm.Model):
    _inherit = "account.invoice"

    _columns = {
        'related_documents': fields.one2many(
            'fatturapa.related_document_type', 'invoice_id',
            'Related Documents'
        ),
        'tax_representative_id': fields.many2one(
            'res.partner', string="Tax Rapresentative"),
        'sender': fields.selection(
            [('CC', 'assignee / partner'), ('TZ', 'third person')], 'Sender'),
        'doc_type': fields.many2one(
            'fatturapa.document_type', string="Document Type"),
        'ftpa_withholding_type': fields.selection(
            [('RT01', 'Natural Person'), ('RT02', 'Legal Person')],
            'Withholding type'
        ),
        'ftpa_withholding_rate': fields.float('Withholding rate'),
        'ftpa_withholding_payment_reason': fields.char(
            'Withholding reason', size=2),
    }
