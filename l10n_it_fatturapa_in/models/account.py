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


class account_invoice(orm.Model):
    _inherit = "account.invoice"

    _columns = {
        'fatturapa_attachment_in_id': fields.many2one(
            'fatturapa.attachment.in', 'FatturaPA Import File',
            ondelete='restrict'),
        'inconsistencies': fields.text('Import Inconsistencies'),
    }


class fatturapa_article_code(orm.Model):
    # _position = ['2.2.1.3']
    _name = "fatturapa.article.code"
    _description = 'FatturaPA Article Code'

    _columns = {
        'name': fields.char('Cod Type', size=35),
        'code_val': fields.char('Code Value', size=35),
        'invoice_line_id': fields.many2one(
            'account.invoice.line', 'Related Invoice line',
            ondelete='cascade', select=True
        )
    }


class account_invoice_line(orm.Model):
    # _position = [
    #     '2.2.1.3', '2.2.1.6', '2.2.1.7',
    #     '2.2.1.8', '2.1.1.10'
    # ]
    _inherit = "account.invoice.line"

    _columns = {
        'cod_article_ids': fields.one2many(
            'fatturapa.article.code', 'invoice_line_id',
            'Cod. Articles'
        ),
        'service_type': fields.selection([
            ('SC', 'sconto'),
            ('PR', 'premio'),
            ('AB', 'abbuono'),
            ('AC', 'spesa accessoria'),
            ], string="Service Type"),
        'ftpa_uom': fields.char('Fattura Pa Unit of Measure', size=10),
        'service_start': fields.date('Service start at'),
        'service_end': fields.date('Service end at'),
        'discount_rise_price_ids': fields.one2many(
            'discount.rise.price', 'invoice_line_id',
            'Discount and Rise Price Details'
        ),
    }
