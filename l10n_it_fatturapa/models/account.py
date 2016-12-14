# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio <davide.corio@abstract.it>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

RELATED_DOCUMENT_TYPES = {
    'order': 'DatiOrdineAcquisto',
    'contract': 'DatiContratto',
    'agreement': 'DatiConvenzione',
    'reception': 'DatiRicezione',
    'invoice': 'DatiFattureCollegate',
}


class FatturapaFormat(models.Model):
    # _position = ['1.1.3']
    _name = "fatturapa.format"
    _description = 'FatturaPA Format'

    name = fields.Char('Description', size=128)
    code = fields.Char('Code', size=5)


class FatturapaDocumentType(models.Model):
    # _position = ['2.1.1.1']
    _name = "fatturapa.document_type"
    _description = 'FatturaPA Document Type'

    name = fields.Char('Description', size=128)
    code = fields.Char('Code', size=4)


class FatturapaPaymentTerm(models.Model):
    # _position = ['2.4.1']
    _name = "fatturapa.payment_term"
    _description = 'FatturaPA Payment Term'

    name = fields.Char('Description', size=128)
    code = fields.Char('Code', size=4)


class FatturapaPaymentMethod(models.Model):
    # _position = ['2.4.2.2']
    _name = "fatturapa.payment_method"
    _description = 'FatturaPA Payment Method'

    name = fields.Char('Description', size=128)
    code = fields.Char('Code', size=4)


#  used in fatturaPa import
class FatturapaPaymentData(models.Model):
    # _position = ['2.4.2.2']
    _name = "fatturapa.payment.data"
    _description = 'FatturaPA Payment Data'

    #  2.4.1
    payment_terms = fields.Many2one(
        'fatturapa.payment_term', string="FatturaPA Payment Method")
    #  2.4.2
    payment_methods = fields.One2many(
        'fatturapa.payment.detail', 'payment_data_id',
        'Payments Details')
    invoice_id = fields.Many2one(
        'account.invoice', 'Related Invoice',
        ondelete='cascade', index=True)


class FatturapaPaymentDetail(models.Model):
    # _position = ['2.4.2']
    _name = "fatturapa.payment.detail"
    recipient = fields.Char('Recipient', size=200)
    fatturapa_pm_id = fields.Many2one(
        'fatturapa.payment_method', string="FatturaPA Payment Method")
    payment_term_start = fields.Date('Payment Term Start')
    payment_days = fields.Integer('Payment Term Days')
    payment_due_date = fields.Date('Payment due Date')
    payment_amount = fields.Float('Payment Amount')
    post_office_code = fields.Char('Post Office Code', size=20)
    recepit_name = fields.Char("Recepit payment partner contact")
    recepit_surname = fields.Char("Recepit payment partner contact")
    recepit_cf = fields.Char("Recepit payment partner contact")
    recepit_title = fields.Char("Recepit payment partner contact")
    payment_bank_name = fields.Char("Bank name")
    payment_bank_iban = fields.Char("IBAN")
    payment_bank_abi = fields.Char("ABI")
    payment_bank_cab = fields.Char("CAB")
    payment_bank_bic = fields.Char("BIC")
    payment_bank = fields.Many2one(
        'res.partner.bank', string="Payment Bank")
    prepayment_discount = fields.Float('Prepayment Discount')
    max_payment_date = fields.Date('Maximum date for Payment')
    penalty_amount = fields.Float('Amount of Penality')
    penalty_date = fields.Date('Effective date of Penality')
    payment_code = fields.Char('Payment code')
    account_move_line_id = fields.Many2one(
        'account.move.line', string="Payment Line")
    payment_data_id = fields.Many2one(
        'fatturapa.payment.data', 'Related payments Data',
        ondelete='cascade', index=True)


#  used in fatturaPa export
class AccountPaymentTerm(models.Model):
    # _position = ['2.4.2.2']
    _inherit = 'account.payment.term'

    fatturapa_pt_id = fields.Many2one(
        'fatturapa.payment_term', string="FatturaPA Payment Term")
    fatturapa_pm_id = fields.Many2one(
        'fatturapa.payment_method', string="FatturaPA Payment Method")


class FatturapaFiscalPosition(models.Model):
    # _position = ['2.1.1.7.7', '2.2.1.14']
    _name = "fatturapa.fiscal_position"
    _description = 'FatturaPA Fiscal Position'

    name = fields.Char('Description', size=128)
    code = fields.Char('Code', size=4)


class WelfareFundType(models.Model):
    # _position = ['2.1.1.7.1']
    _name = "welfare.fund.type"
    _description = 'welfare fund type'

    name = fields.Char('name')
    description = fields.Char('description')


class WelfareFundDataLine(models.Model):
    # _position = ['2.1.1.7']
    _name = "welfare.fund.data.line"
    _description = 'FatturaPA Welfare Fund Data'

    name = fields.Many2one(
        'welfare.fund.type', string="Welfare Fund Type")
    kind_id = fields.Many2one('account.tax.kind', string="Non taxable nature")
    welfare_rate_tax = fields.Float('Welfare Rate tax')
    welfare_amount_tax = fields.Float('Welfare Amount tax')
    welfare_taxable = fields.Float('Welfare Taxable')
    welfare_Iva_tax = fields.Float('Welfare  tax')
    subjected_withholding = fields.Char(
        'Subjected at Withholding', size=2)
    pa_line_code = fields.Char('PA Code for this record', size=20)
    invoice_id = fields.Many2one(
        'account.invoice', 'Related Invoice',
        ondelete='cascade', index=True
    )


class DiscountRisePrice(models.Model):
    # _position = ['2.1.1.8', '2.2.1.10']
    _name = "discount.rise.price"
    _description = 'FatturaPA Discount Rise Price Data'

    name = fields.Selection(
        [('SC', 'Discount'), ('MG', 'Rise Price')], 'Type')
    percentage = fields.Float('Percentage')
    amount = fields.Float('Amount')
    invoice_id = fields.Many2one(
        'account.invoice.line', 'Related Invoice',
        ondelete='cascade', index=True
    )


class FatturapaRelatedDocumentType(models.Model):
    # _position = ['2.1.2', '2.2.3', '2.1.4', '2.1.5', '2.1.6']
    _name = 'fatturapa.related_document_type'
    _description = 'FatturaPA Related Document Type'

    type = fields.Selection(
        [
            ('order', 'Order'),
            ('contract', 'Contract'),
            ('agreement', 'Agreement'),
            ('reception', 'Reception'),
            ('invoice', 'Related Invoice')
        ],
        'Document Type', required=True
    )
    name = fields.Char('DocumentID', size=20, required=True)
    lineRef = fields.Integer('LineRef')
    invoice_line_id = fields.Many2one(
        'account.invoice.line', 'Related Invoice Line',
        ondelete='cascade', index=True)
    invoice_id = fields.Many2one(
        'account.invoice', 'Related Invoice',
        ondelete='cascade', index=True)
    date = fields.Date('Date')
    numitem = fields.Char('NumItem', size=20)
    code = fields.Char('Order Agreement Code', size=100)
    cig = fields.Char('CIG Code', size=15)
    cup = fields.Char('CUP Code', size=15)

    @api.model
    def create(self, vals):
        if vals.get('invoice_line_id'):
            line_obj = self.env['account.invoice.line']
            line = line_obj.browse(vals['invoice_line_id'])
            vals['lineRef'] = line.sequence
        return super(FatturapaRelatedDocumentType, self).create(vals)


class FaturapaActivityProgress(models.Model):
    # _position = ['2.1.7']
    _name = "faturapa.activity.progress"

    fatturapa_activity_progress = fields.Integer('Activity Progress')
    invoice_id = fields.Many2one(
        'account.invoice', 'Related Invoice',
        ondelete='cascade', index=True)


class FatturaAttachments(models.Model):
    # _position = ['2.5']
    _name = "fatturapa.attachments"
    _description = "FatturaPA attachments"
    _inherits = {'ir.attachment': 'ir_attachment_id'}

    ir_attachment_id = fields.Many2one(
        'ir.attachment', 'Attachment', required=True, ondelete="cascade")
    compression = fields.Char('Compression', size=10)
    format = fields.Char('Format', size=10)
    invoice_id = fields.Many2one(
        'account.invoice', 'Related Invoice',
        ondelete='cascade', index=True)


class FatturapaRelatedDdt(models.Model):
    # _position = ['2.1.2', '2.2.3', '2.1.4', '2.1.5', '2.1.6']
    _name = 'fatturapa.related_ddt'
    _description = 'FatturaPA Related DdT'

    name = fields.Char('DocumentID', size=20, required=True)
    date = fields.Date('Date')
    lineRef = fields.Integer('LineRef')
    invoice_line_id = fields.Many2one(
        'account.invoice.line', 'Related Invoice Line',
        ondelete='cascade', index=True)
    invoice_id = fields.Many2one(
        'account.invoice', 'Related Invoice',
        ondelete='cascade', index=True)

    @api.model
    def create(self, vals):
        if vals.get('invoice_line_id'):
            line_obj = self.env['account.invoice.line']
            line = line_obj.browse(vals['invoice_line_id'])
            vals['lineRef'] = line.sequence
        return super(FatturapaRelatedDdt, self).create(vals)


class AccountInvoiceLine(models.Model):
    # _position = ['2.2.1']
    _inherit = "account.invoice.line"

    related_documents = fields.One2many(
        'fatturapa.related_document_type', 'invoice_line_id',
        'Related Documents Type'
    )
    ftpa_related_ddts = fields.One2many(
        'fatturapa.related_ddt', 'invoice_line_id',
        'Related DdT'
    )
    admin_ref = fields.Char('Administration ref.', size=20)


class FaturapaSummaryData(models.Model):
    # _position = ['2.2.2']
    _name = "faturapa.summary.data"
    tax_rate = fields.Float('Tax Rate')
    non_taxable_nature = fields.Selection([
        ('N1', 'escluse ex art. 15'),
        ('N2', 'non soggette'),
        ('N3', 'non imponibili'),
        ('N4', 'esenti'),
        ('N5', 'regime del margine'),
        ('N6', 'inversione contabile (reverse charge)'),
    ], string="Non taxable nature")
    incidental_charges = fields.Float('Incidental Charges')
    rounding = fields.Float('Rounding')
    amount_untaxed = fields.Float('Amount untaxed')
    amount_tax = fields.Float('Amount tax')
    payability = fields.Selection([
        ('I', 'Immediate payability'),
        ('D', 'Deferred payability'),
        ('S', 'Split payment'),
    ], string="VAT payability")
    law_reference = fields.Char(
        'Law reference', size=128)
    invoice_id = fields.Many2one(
        'account.invoice', 'Related Invoice',
        ondelete='cascade', index=True)


class AccountInvoice(models.Model):
    # _position = ['2.1', '2.2', '2.3', '2.4', '2.5']
    _inherit = "account.invoice"
    protocol_number = fields.Char('Protocol Number', size=64)
    # 1.2 -- partner_id
    # 1.3
    tax_representative_id = fields.Many2one(
        'res.partner', string="Tax Rapresentative")
    #  1.4 company_id
    #  1.5
    intermediary = fields.Many2one(
        'res.partner', string="Intermediary")
    #  1.6
    sender = fields.Selection(
        [('CC', 'assignee / partner'), ('TZ', 'third person')], 'Sender')
    #  2.1.1.1
    doc_type = fields.Many2one(
        'fatturapa.document_type', string="Document Type")
    #  2.1.1.5
    #  2.1.1.5.1
    ftpa_withholding_type = fields.Selection(
        [('RT01', 'Natural Person'), ('RT02', 'Legal Person')],
        'Withholding type'
    )
    #  2.1.1.5.2 withholding_amount in module
    #  2.1.1.5.3
    ftpa_withholding_rate = fields.Float('Withholding rate')
    #  2.1.1.5.4
    ftpa_withholding_payment_reason = fields.Char(
        'Withholding reason', size=2)
    #  2.1.1.6
    virtual_stamp = fields.Boolean('Virtual Stamp', default=False)
    stamp_amount = fields.Float('Stamp Amount')
    #  2.1.1.7
    welfare_fund_ids = fields.One2many(
        'welfare.fund.data.line', 'invoice_id',
        'Welfare Fund'
    )
    #  2.1.1.8
    discount_rise_price_ids = fields.One2many(
        'discount.rise.price', 'invoice_id',
        'Discount and Rise Price Details'
    )
    #  2.1.2 - 2.1.6
    related_documents = fields.One2many(
        'fatturapa.related_document_type', 'invoice_id',
        'Related Documents'
    )
    #  2.1.7
    activity_progress_ids = fields.One2many(
        'faturapa.activity.progress', 'invoice_id',
        'Fase of Activity Progress'
    )
    #  2.1.8
    ftpa_related_ddts = fields.One2many(
        'fatturapa.related_ddt', 'invoice_id',
        'Related DdT'
    )
    #  2.1.9
    carrier_id = fields.Many2one(
        'res.partner', string="Carrier")
    transport_vaicle = fields.Char('Veicle', size=80)
    transport_reason = fields.Char('Reason', size=80)
    number_items = fields.Integer('number of items')
    description = fields.Char('Description', size=100)
    unit_weight = fields.Char('Weight unit', size=10)
    gross_weight = fields.Float('Gross Weight')
    net_weight = fields.Float('Net Weight')
    pickup_datetime = fields.Datetime('Pick up')
    transport_date = fields.Date('Transport Date')
    delivery_address = fields.Text('Delivery Address')
    delivery_datetime = fields.Datetime('Delivery Date Time')
    #  2.1.10
    related_invoice_code = fields.Char('Related invoice code')
    related_invoice_date = fields.Date('Related invoice date')
    #  2.2.1 invoice lines
    #  2.2.2
    fatturapa_summary_ids = fields.One2many(
        'faturapa.summary.data', 'invoice_id',
        'FatturaPA Summary Datas'
    )
    #  2.3
    vaicle_registration = fields.Date('Veicole Registration')
    total_travel = fields.Char('Travel in hours or Km', size=15)
    #  2.4
    fatturapa_payments = fields.One2many(
        'fatturapa.payment.data', 'invoice_id',
        'FatturaPA Payment Datas'
    )
    #  2.5
    fatturapa_doc_attachments = fields.One2many(
        'fatturapa.attachments', 'invoice_id',
        'FatturaPA attachments'
    )
