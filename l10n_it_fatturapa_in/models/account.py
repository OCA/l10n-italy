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
from openerp.addons import decimal_precision as dp


class account_invoice(orm.Model):
    _inherit = "account.invoice"

    _columns = {
        'fatturapa_attachment_in_id': fields.many2one(
            'fatturapa.attachment.in', 'FatturaPA Import File',
            ondelete='restrict'),
        'inconsistencies': fields.text('Import Inconsistencies'),
        
        'e_invoice_line_ids': fields.one2many(
            "einvoice.line", "invoice_id", string="Dettaglio Linee",
            readonly=True, copy=False),
    'e_invoice_amount_untaxed': fields.float(
        string='E-Invoice Untaxed Amount', readonly=True),
    'e_invoice_amount_tax': fields.float(string='E-Invoice Tax Amount',
                                           readonly=True),
    'e_invoice_amount_total': fields.float(string='E-Invoice Total Amount',
                                             readonly=True),

    'e_invoice_reference': fields.char(
        string="E-invoice vendor reference",
        readonly=True),

    'e_invoice_date_invoice': fields.date(
        string="E-invoice invoice date",
        readonly=True),

    'e_invoice_validation_error': fields.boolean(
        compute='_compute_e_invoice_validation_error'),

    'e_invoice_validation_message': fields.text(
        compute='_compute_e_invoice_validation_error'),

    'e_invoice_force_validation': fields.boolean(
        string='Force E-Invoice Validation'),

    'e_invoice_received_date': fields.date(
        string='E-Bill Received Date'),
    }

    def name_get(self, cr, uid, ids, context={}):
        result = super(account_invoice, self).name_get(cr, uid, ids, context)
        res = []
        for tup in result:
            invoice = self.browse(cr, uid, tup[0])
            if invoice.type in ('in_invoice', 'in_refund'):
                name = "%s, %s" % (tup[1], invoice.partner_id.name)
                if invoice.origin:
                    name += ', %s' % invoice.origin
                res.append((invoice.id, name))
            else:
                res.append(tup)
        return res

    def remove_attachment_link(self, cr, uid, ids, context={}):
        self.write(cr, uid, ids, {'fatturapa_attachment_in_id': False}, context)
        return {'type': 'ir.actions.client', 'tag': 'reload'}


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
        ),
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
        
        'fatturapa_attachment_in_id': fields.related(
            'invoice_id', 'fatturapa_attachment_in_id', type='many2one',
            relation='fatturapa.attachment.in', string='E-Invoice Import File'),
    }


class DiscountRisePrice(orm.Model):
    _inherit = "discount.rise.price"
    
    _columns = {
        'e_invoice_line_id': fields.many2one(
            'einvoice.line', 'Related E-Invoice line', readonly=True
            )
    }


class EInvoiceLine(orm.Model):
    _name = 'einvoice.line'

    _columns = {
        'invoice_id': fields.many2one(
            "account.invoice", "Invoice", readonly=True),
        'line_number': fields.integer('Numero Linea', readonly=True),
        'service_type': fields.char('Tipo Cessione Prestazione', readonly=True),
        'cod_article_ids': fields.one2many(
            'fatturapa.article.code', 'invoice_line_id',
            'Cod. Articles', readonly=True
        ),
        'name': fields.char("Descrizione", readonly=True),
        'qty': fields.float(
            "Quantita'", readonly=True,
            digits_compute=dp.get_precision('Product Unit of Measure')
        ),
        'uom': fields.char("Unita' di misura", readonly=True),
        'period_start_date': fields.date("Data Inizio Periodo", readonly=True),
        'period_end_date': fields.date("Data Fine Periodo", readonly=True),
        'unit_price': fields.float(
            "Prezzo unitario", readonly=True,
            digits_compute=dp.get_precision('Product Price')
        ),
        'discount_rise_price_ids': fields.one2many(
            'discount.rise.price', 'e_invoice_line_id',
            'Discount and Rise Price Details', readonly=True
        ),
        'total_price': fields.float("Prezzo Totale", readonly=True),
        'tax_amount': fields.float("Aliquota IVA", readonly=True),
        'wt_amount': fields.char("Ritenuta", readonly=True),
        'tax_kind': fields.char("Natura", readonly=True),
        'admin_ref': fields.char("Riferimento mministrazione", readonly=True),
        'other_data_ids': fields.one2many(
            "einvoice.line.other.data", "e_invoice_line_id",
            string="Altri dati gestionali", readonly=True),
    }


class EInvoiceLineOtherData(orm.Model):
    _name = 'einvoice.line.other.data'

    _columns = {
        'e_invoice_line_id': fields.many2one(
            'einvoice.line', 'Related E-Invoice line', readonly=True
        ),
        'name': fields.char("Tipo Dato", readonly=True),
        'text_ref': fields.char("Riferimento Testo", readonly=True),
        'num_ref': fields.float("Riferimento Numero", readonly=True),
        'date_ref': fields.char("Riferimento Data", readonly=True),
    }
