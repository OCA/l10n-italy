# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Davide Corio <davide.corio@lsweb.it>
#    Copyright (C) 2018 Copyright (C) OmniaSolutions (<http://www.omniasolutions.eu>). All Rights Reserved
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

from openerp.osv import fields
from openerp.osv import orm


RELATED_DOCUMENT_TYPES = {
    'order': 'DatiOrdineAcquisto',
    'contract': 'DatiContratto',
    'agreement': 'DatiConvenzione',
    'reception': 'DatiRicezione',
    'invoice': 'DatiFattureCollegate',
}


class fatturapa_format(orm.Model):
    # _position = ['1.1.3']
    _name = "fatturapa.format"
    _description = 'E-invoice Format'

    _columns = {
        'name': fields.char('Description', size=128),
        'code': fields.char('Code', size=5),
    }


class fatturapa_document_type(orm.Model):
    # _position = ['2.1.1.1']
    _name = "fatturapa.document_type"
    _description = 'E-invoice Document Type'

    _columns = {
        'name': fields.char('Description', size=128),
        'code': fields.char('Code', size=4),
    }


#  used in fatturaPa import
class fatturapa_payment_data(orm.Model):
    # _position = ['2.4.2.2']
    _name = "fatturapa.payment.data"
    _description = 'E-invoice Payment Data'

    _columns = {
        #  2.4.1
        'payment_terms': fields.many2one(
            'fatturapa.payment_term', string="Electronic Invoice Payment Method"),
        #  2.4.2
        'payment_methods': fields.one2many(
            'fatturapa.payment.detail', 'payment_data_id',
            'Payments Details'
        ),
        'invoice_id': fields.many2one(
            'account.invoice', 'Related Invoice',
            ondelete='cascade', select=True),
    }


class fatturapa_payment_detail(orm.Model):
    # _position = ['2.4.2']
    _name = "fatturapa.payment.detail"
    _description = "E-invoice payment details"
    _columns = {
        'recipient': fields.char('Recipient', size=200),
        'fatturapa_pm_id': fields.many2one(
            'fatturapa.payment_method', string="Electronic Invoice Payment Method"),
        'payment_term_start': fields.date('Payment Term Start'),
        'payment_days': fields.integer('Payment Term Days'),
        'payment_due_date': fields.date('Payment due Date'),
        'payment_amount': fields.float('Payment Amount'),
        'post_office_code': fields.char('Post Office Code', size=20),
        'recepit_name': fields.char("Receipt Issuer Name"),
        'recepit_surname': fields.char("Receipt Issuer Surname"),
        'recepit_cf': fields.char("Receipt Issuer FC"),
        'recepit_title': fields.char("Receipt Issuer Title"),
        'payment_bank_name': fields.char("Bank name"),
        'payment_bank_iban': fields.char("IBAN"),
        'payment_bank_abi': fields.char("ABI"),
        'payment_bank_cab': fields.char("CAB"),
        'payment_bank_bic': fields.char("BIC"),
        'payment_bank': fields.many2one(
            'res.partner.bank', string="Payment Bank"),
        'prepayment_discount': fields.float('Prepayment Discount'),
        'max_payment_date': fields.date('Maximum date for Payment'),
        'penalty_amount': fields.float('Amount of Penality'),
        'penalty_date': fields.date('Effective date of Penality'),
        'payment_code': fields.char('Payment code'),
        'account_move_line_id': fields.many2one(
            'account.move.line', string="Payment Line"),
        'payment_data_id': fields.many2one(
            'fatturapa.payment.data', 'Related Payments Data',
            ondelete='cascade', select=True),
    }


class fatturapa_fiscal_position(orm.Model):
    # _position = ['2.1.1.7.7', '2.2.1.14']
    _name = "fatturapa.fiscal_position"
    _description = 'Electronic Invoice Fiscal Position'

    _columns = {
        'name': fields.char('Description', size=128),
        'code': fields.char('Code', size=4),
    }


class welfare_fund_type(orm.Model):
    # _position = ['2.1.1.7.1']
    _name = "welfare.fund.type"
    _description = 'Welfare Fund Type'

    _columns = {
        'name': fields.char('name'),
        'description': fields.char('description'),
    }

    def name_get(self, cr, uid, ids, context={}):
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            res.append(
                (record.id, u'[%s] %s' % (record.name, record.description)))
        return res


class welfare_fund_data_line(orm.Model):
    # _position = ['2.1.1.7']
    _name = "welfare.fund.data.line"
    _description = 'E-invoice Welfare Fund Data'

    _columns = {
        'name': fields.many2one(
            'welfare.fund.type', string="Welfare Fund Type"),
        'kind_id': fields.many2one('account.tax.kind', string="Non taxable nature"),
        'fund_nature': fields.selection([
            ('N1', 'escluse ex art. 15'),
            ('N2', 'non soggette'),
            ('N3', 'non imponibili'),
            ('N4', 'esenti'),
            ('N5', 'regime del margine'),
            ('N6', 'inversione contabile (reverse charge)'),
        ], string="Non taxable nature"),
        #TODO: Il campo fund_nature è stato sostiruito con kind_id = fields.Many2one('account.tax.kind', string="Non taxable nature")
        # Se mettiamo questo campo è necessario decommentarlo dalla vista l10n_it_fatturapa_in/views/account_view.xml
        # kind_id = fields.Many2one('account.tax.kind', string="Non taxable nature")
        'welfare_rate_tax': fields.float('Welfare Rate tax'),
        'welfare_amount_tax': fields.float('Welfare Amount tax'),
        'welfare_taxable': fields.float('Welfare Taxable'),
        'welfare_Iva_tax': fields.float('Welfare  tax'),
        'subjected_withholding': fields.char(
            'Subjected at Withholding', size=2),
        'pa_line_code': fields.char('PA Code for this record', size=20),
        'invoice_id': fields.many2one(
            'account.invoice', 'Related Invoice',
            ondelete='cascade', select=True
        ),
    }


class discount_rise_price(orm.Model):
    # _position = ['2.1.1.8', '2.2.1.10']
    _name = "discount.rise.price"
    _description = 'FatturaPA Discount Rise Price Data'

    _columns = {
        'name': fields.selection(
            [('SC', 'Discount'), ('MG', 'Rise Price')], 'Type'),
        'percentage': fields.float('Percentage'),
        'amount': fields.float('Amount'),
        'invoice_id': fields.many2one(
            'account.invoice', 'Related Invoice',
            ondelete='cascade', select=True
        ),
        'invoice_line_id': fields.many2one(
            'account.invoice.line', 'Related Invoice line',
            ondelete='cascade', select=True
        ),
    }


class fatturapa_related_document_type(orm.Model):
    # _position = ['2.1.2', '2.2.3', '2.1.4', '2.1.5', '2.1.6']
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
        'cig': fields.char('CIG Code', size=15),
        'cup': fields.char('CUP Code', size=15),
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


class faturapa_activity_progress(orm.Model):
    # _position = ['2.1.7']
    _name = "faturapa.activity.progress"

    _columns = {
        'fatturapa_activity_progress': fields.integer('Activity Progress'),
        'invoice_id': fields.many2one(
            'account.invoice', 'Related Invoice',
            ondelete='cascade', select=True)
    }


class fattura_attachments(orm.Model):
    # _position = ['2.5']
    _name = "fatturapa.attachments"
    _description = "E-invoice attachments"
    _inherits = {'ir.attachment': 'ir_attachment_id'}

    _columns = {
        'ir_attachment_id': fields.many2one(
            'ir.attachment', 'Attachment', required=True, ondelete="cascade"),
        'compression': fields.char('Compression', size=10),
        'format': fields.char('Format', size=10),
        'invoice_id': fields.many2one(
            'account.invoice', 'Related Invoice',
            ondelete='cascade', select=True)
    }


class fatturapa_related_ddt(orm.Model):
    # _position = ['2.1.2', '2.2.3', '2.1.4', '2.1.5', '2.1.6']
    _name = 'fatturapa.related_ddt'
    _description = 'E-invoice Related DDT'

    _columns = {
        'name': fields.char('DocumentID', size=20, required=True),
        'date': fields.date('Date'),
        'lineRef': fields.integer('LineRef'),
        'invoice_line_id': fields.many2one(
            'account.invoice.line', 'Related Invoice Line',
            ondelete='cascade', select=True),
        'invoice_id': fields.many2one(
            'account.invoice', 'Related Invoice',
            ondelete='cascade', select=True),
    }

    def create(self, cr, uid, vals, context=None):
        if not context:
            context = {}
        if vals.get('invoice_line_id'):
            line_obj = self.pool.get('account.invoice.line')
            line = line_obj.browse(
                cr, uid, vals['invoice_line_id'], context=context)
            vals['lineRef'] = line.sequence
        return super(fatturapa_related_ddt, self).\
            create(cr, uid, vals, context)


class account_invoice_line(orm.Model):
    # _position = ['2.2.1']
    _inherit = "account.invoice.line"

    _columns = {
        'related_documents': fields.one2many(
            'fatturapa.related_document_type', 'invoice_line_id',
            'Related Documents Type'
        ),
        'ftpa_related_ddts': fields.one2many(
            'fatturapa.related_ddt', 'invoice_line_id',
            'Related DdT'
        ),
        'admin_ref': fields.char('Administration ref.', size=20),
        
        
        
    'discount_rise_price_ids': fields.one2many(
        'discount.rise.price', 'invoice_line_id',
        'Discount or Supplement Price Details', copy=False
    ),
    'ftpa_line_number': fields.integer("Line number", readonly=True, copy=False) ,
    }


class faturapa_summary_data(orm.Model):
    # _position = ['2.2.2']
    _name = "faturapa.summary.data"
    _columns = {
        'tax_rate': fields.float('Tax Rate'),
        'non_taxable_nature': fields.selection([
        ('N1', 'excluded pursuant to Art. 15'),
        ('N2', 'not subject'),
        ('N2.1', 'not subject to VAT under the articles from 7 to '
                 '7-septies of DPR 633/72'),
        ('N2.2', 'not subject – other cases'),
        ('N3', 'not taxable'),
        ('N3.1', 'not taxable – exportations'),
        ('N3.2', 'not taxable – intra Community transfers'),
        ('N3.3', 'not taxable – transfers to San Marino'),
        ('N3.4', 'not taxable – transactions treated as export supplies'),
        ('N3.5', 'not taxable – for declaration of intent'),
        ('N3.6', 'not taxable – other transactions that don’t contribute to the '
                 'determination of ceiling'),
        ('N4', 'exempt'),
        ('N5', 'margin regime'),
        ('N6', 'reverse charge'),
        ('N6.1', 'reverse charge – transfer of scrap and of other recyclable '
                 'materials'),
        ('N6.2', 'reverse charge – transfer of gold and pure silver'),
        ('N6.3', 'reverse charge – subcontracting in the construction sector'),
        ('N6.4', 'reverse charge – transfer of buildings'),
        ('N6.5', 'reverse charge – transfer of mobile phones'),
        ('N6.6', 'reverse charge – transfer of electronic products'),
        ('N6.7', 'reverse  charge – provisions in the construction and related '
                 'sectors'),
        ('N6.8', 'reverse charge – transactions in the energy sector'),
        ('N6.9', 'reverse charge – other cases'),
        ('N7', 'VAT paid in other EU countries'),
    ], string="Non taxable nature"),
        'incidental_charges': fields.float('Incidental Charges'),
        'rounding': fields.float('Rounding'),
        'amount_untaxed': fields.float('Amount untaxed'),
        'amount_tax': fields.float('Amount tax'),
        'payability': fields.selection([
            ('I', 'Immediate payability'),
            ('D', 'Deferred payability'),
            ('S', 'Split payment'),
        ], string="VAT payability"),
        'law_reference': fields.char(
            'Law reference', size=128),
        'invoice_id': fields.many2one(
            'account.invoice', 'Related Invoice',
            ondelete='cascade', select=True)
    }


class account_invoice(orm.Model):
    # _position = ['2.1', '2.2', '2.3', '2.4', '2.5']
    _inherit = "account.invoice"
    _columns = {
        'protocol_number': fields.char('Protocol Number', size=64),
        # 1.2 -- partner_id
        #  1.3
        'tax_representative_id': fields.many2one(
            'res.partner', string="Tax Rapresentative"),
        #  1.4 company_id
        #  1.5
        'intermediary': fields.many2one(
            'res.partner', string="Intermediary"),
        #  1.6
        'sender': fields.selection(
            [('CC', 'assignee / partner'), ('TZ', 'third person')], 'Sender'),
        
        'ftpa_withholding_ids': fields.one2many(
            'withholding.data.line', 'invoice_id',
            'Withholding'
            ),
        'welfare_fund_ids': fields.one2many(
            'welfare.fund.data.line', 'invoice_id',
            'Welfare Fund'
        ),
        #  2.1.1.1
        'doc_type': fields.many2one(
            'fatturapa.document_type', string="Document Type"),
        #  2.1.1.5
        #  2.1.1.5.1
        'ftpa_withholding_type': fields.selection(
            [('RT01', 'Natural Person'), ('RT02', 'Legal Person')],
            'Withholding type'
        ),
        #  2.1.1.5.2 withholding_amount in module
        #  2.1.1.5.3
        'ftpa_withholding_rate': fields.float('Withholding rate'),
        #  2.1.1.5.4
        'ftpa_withholding_payment_reason': fields.char(
            'Withholding reason', size=2),
        #  2.1.1.6
        'virtual_stamp': fields.boolean('Virtual Stamp'),
        'stamp_amount': fields.float('Stamp Amount'),
        #  2.1.1.8
        'discount_rise_price_ids': fields.one2many(
            'discount.rise.price', 'invoice_id',
            'Discount and Rise Price Details'
        ),
        #  2.1.2 - 2.1.6
        'related_documents': fields.one2many(
            'fatturapa.related_document_type', 'invoice_id',
            'Related Documents'
        ),
        #  2.1.7
        'activity_progress_ids': fields.one2many(
            'faturapa.activity.progress', 'invoice_id',
            'Fase of Activity Progress'
        ),
        #  2.1.8
        'ftpa_related_ddts': fields.one2many(
            'fatturapa.related_ddt', 'invoice_id',
            'Related DdT'
        ),
        #  2.1.9
        'carrier_id': fields.many2one(
            'res.partner', string="Carrier"),
        'transport_vehicle': fields.char('Vehicle', size=80),
        'transport_reason': fields.char('Reason', size=80),
        'number_items': fields.integer('number of items'),
        'description': fields.char('Description', size=100),
        'unit_weight': fields.char('Weight unit', size=10),
        'gross_weight': fields.float('Gross Weight'),
        'net_weight': fields.float('Net Weight'),
        'pickup_datetime': fields.datetime('Pick up'),
        'transport_date': fields.date('Transport Date'),
        'delivery_address': fields.text('Delivery Address'),
        'delivery_datetime': fields.datetime('Delivery Date Time'),
        
        
        'ftpa_incoterms': fields.char(string="Incoterms", copy=False),

        #  2.1.10
        'related_invoice_code': fields.char('Related invoice code'),
        'related_invoice_date': fields.date('Related invoice date'),
        #  2.2.1 invoice lines
        #  2.2.2
        'fatturapa_summary_ids': fields.one2many(
            'faturapa.summary.data', 'invoice_id',
            'FatturaPA Summary   Datas'
        ),
        #  2.3
        'Vehicle_registration': fields.date('Veicole Registration'),
        'total_travel': fields.char('Travel in hours or Km', size=15),
        #  2.4
        'fatturapa_payments': fields.one2many(
            'fatturapa.payment.data', 'invoice_id',
            'FatturaPA Payment Datas'
        ),
        #  2.5
        'fatturapa_doc_attachments': fields.one2many(
            'fatturapa.attachments', 'invoice_id',
            'FatturaPA attachments'
        ),
        
    'efatt_stabile_organizzazione_indirizzo': fields.char(
        string="Indirizzo Organizzazione",
        help="Blocco da valorizzare nei casi di cedente / prestatore non "
             "residente, con stabile organizzazione in Italia. Indirizzo "
             "della stabile organizzazione in Italia (nome della via, piazza "
             "etc.)",
        readonly=True, copy=False),
    'efatt_stabile_organizzazione_civico': fields.char(
        string="Civico Organizzazione",
        help="Numero civico riferito all'indirizzo (non indicare se gia' "
             "presente nell'elemento informativo indirizzo)",
        readonly=True, copy=False),
    'efatt_stabile_organizzazione_cap': fields.char(
        string="CAP Organizzazione",
        help="Codice Avviamento Postale",
        readonly=True, copy=False),
    'efatt_stabile_organizzazione_comune': fields.char(
        string="Comune Organizzazione",
        help="Comune relativo alla stabile organizzazione in Italia",
        readonly=True, copy=False),
    'efatt_stabile_organizzazione_provincia': fields.char(
        string="Provincia Organizzazione",
        help="Sigla della provincia di appartenenza del comune indicato "
             "nell'elemento informativo 1.2.3.4 <Comune>. Da valorizzare se "
             "l'elemento informativo 1.2.3.6 <Nazione> e' uguale a IT",
        readonly=True, copy=False),
    'efatt_stabile_organizzazione_nazione': fields.char(
        string="Nazione Organizzazione",
        help="Codice della nazione espresso secondo lo standard "
             "ISO 3166-1 alpha-2 code",
        readonly=True, copy=False),
    # 2.1.1.10
    'efatt_rounding': fields.float(
        "Arrotondamento", readonly=True,
        help="Eventuale arrotondamento sul totale documento (ammette anche il "
             "segno negativo)", copy=False
    ),
    'art73': fields.boolean(
        'Art73', readonly=True,
        help="Indica se il documento e' stato emesso secondo modalita' e "
             "termini stabiliti con decreto ministeriale ai sensi "
             "dell'articolo 73 del DPR 633/72 (cio' consente al "
             "cedente/prestatore l'emissione nello stesso anno di piu' "
             "documenti aventi stesso numero)", copy=False),
    'electronic_invoice_subjected': fields.related('partner_id', 'electronic_invoice_subjected',
                                                type='boolean', relation='res.partner',
                                                string='Subjected to electronic invoice', readonly=True),
    
    }
    _defaults = {
        'virtual_stamp': False
    }

    def copy(self, cr, uid, id, default=None, context=None):
        default['fatturapa_attachment_out_id'] = False
        ret_id = super(account_invoice, self).copy(cr, uid, id, default, context=context)
        return ret_id

class fatturapa_payment_term(orm.Model):
    # _position = ['2.4.1']
    _name = "fatturapa.payment_term"
    _description = 'FatturaPA Payment Term'

    _columns = {
        'name': fields.char('Description', size=128),
        'code': fields.char('Code', size=4),
    }


class fatturapa_payment_method(orm.Model):
    # _position = ['2.4.2.2']
    _name = "fatturapa.payment_method"
    _description = 'FatturaPA Payment Method'

    _columns = {
        'name': fields.char('Description', size=128),
        'code': fields.char('Code', size=4),
    }

#  used in fatturaPa export
class account_payment_term(orm.Model):
    # _position = ['2.4.2.2']
    _inherit = 'account.payment.term'

    _columns = {
        'fatturapa_pt_id': fields.many2one(
            'fatturapa.payment_term', string="FatturaPA Payment Term"),
        'fatturapa_pm_id': fields.many2one(
            'fatturapa.payment_method', string="FatturaPA Payment Method"),
    }

class WithholdingDataLine(orm.Model):
    _name = "withholding.data.line"
    _description = 'E-invoice Withholding Data'

    _columns = {
        'name': fields.selection(
            selection=[
                ('RT01', 'Natural Person'),
                ('RT02', 'Legal Person'),
                ('RT03', 'INPS'),
                ('RT04', 'ENASARCO'),
                ('RT05', 'ENPAM'),
                ('RT06', 'OTHER'),
            ],
            string='Withholding Type'
        ),
        'amount': fields.float('Withholding amount'),
        'rate': fields.float('Withholding rate'),
        'reason': fields.char('Withholding reason'),
        'invoice_id': fields.many2one(
            'account.invoice', 'Related Invoice',
            ondelete='cascade', index=True
        ),
    }