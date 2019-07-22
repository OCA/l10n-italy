# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import odoo.addons.decimal_precision as dp
from odoo.tools import float_compare


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    fatturapa_attachment_in_id = fields.Many2one(
        'fatturapa.attachment.in', 'E-bill Import File',
        ondelete='restrict', copy=False)
    inconsistencies = fields.Text('Import Inconsistencies', copy=False)
    e_invoice_line_ids = fields.One2many(
        "einvoice.line", "invoice_id", string="Lines Detail",
        readonly=True, copy=False)

    e_invoice_amount_untaxed = fields.Monetary(
        string='E-Invoice Untaxed Amount', readonly=True)
    e_invoice_amount_tax = fields.Monetary(string='E-Invoice Tax Amount',
                                           readonly=True)
    e_invoice_amount_total = fields.Monetary(string='E-Invoice Total Amount',
                                             readonly=True)

    e_invoice_reference = fields.Char(
        string="E-invoice vendor reference",
        readonly=True)

    e_invoice_date_invoice = fields.Date(
        string="E-invoice invoice date",
        readonly=True)

    e_invoice_validation_error = fields.Boolean(
        compute='_compute_e_invoice_validation_error')

    e_invoice_validation_message = fields.Text(
        compute='_compute_e_invoice_validation_error')

    e_invoice_force_validation = fields.Boolean(
        string='Force E-Invoice Validation')

    @api.multi
    def invoice_validate(self):
        for invoice in self:
            if (invoice.e_invoice_validation_error and
                    not invoice.e_invoice_force_validation):
                raise ValidationError(
                    _("The invoice '%s' doesn't match the related e-invoice") %
                    invoice.display_name)
        return super(AccountInvoice, self).invoice_validate()

    @api.depends('type', 'state', 'fatturapa_attachment_in_id',
                 'amount_untaxed', 'amount_tax', 'amount_total',
                 'reference', 'date_invoice')
    def _compute_e_invoice_validation_error(self):
        bills_to_check = self.filtered(
            lambda inv:
                inv.type in ['in_invoice', 'in_refund'] and
                inv.state in ['draft', 'open', 'paid'] and
                inv.fatturapa_attachment_in_id)
        for bill in bills_to_check:
            error_messages = list()
            if (bill.e_invoice_amount_untaxed and
                    float_compare(bill.amount_untaxed,
                                  bill.e_invoice_amount_untaxed,
                                  precision_rounding=bill.currency_id
                                  .rounding) != 0):
                error_messages.append(
                    _("Untaxed amount ({bill_amount_untaxed}) "
                      "does not match with "
                      "e-bill untaxed amount ({e_bill_amount_untaxed})")
                    .format(
                        bill_amount_untaxed=bill.amount_untaxed or 0,
                        e_bill_amount_untaxed=bill.e_invoice_amount_untaxed
                    ))

            if (bill.e_invoice_amount_tax and
                    float_compare(bill.amount_tax,
                                  bill.e_invoice_amount_tax,
                                  precision_rounding=bill.currency_id
                                  .rounding) != 0):
                error_messages.append(
                    _("Taxed amount ({bill_amount_tax}) "
                      "does not match with "
                      "e-bill taxed amount ({e_bill_amount_tax})")
                    .format(
                        bill_amount_tax=bill.amount_tax or 0,
                        e_bill_amount_tax=bill.e_invoice_amount_tax
                    ))

            if (bill.e_invoice_amount_total and
                    float_compare(bill.amount_total,
                                  bill.e_invoice_amount_total,
                                  precision_rounding=bill.currency_id
                                  .rounding) != 0):
                error_messages.append(
                    _("Total amount ({bill_amount_total}) "
                      "does not match with "
                      "e-bill total amount ({e_bill_amount_total})")
                    .format(
                        bill_amount_total=bill.amount_total or 0,
                        e_bill_amount_total=bill.e_invoice_amount_total
                    ))

            if (bill.e_invoice_reference and
                    bill.reference != bill.e_invoice_reference):
                error_messages.append(
                    _("Vendor reference ({bill_vendor_ref}) "
                      "does not match with "
                      "e-bill vendor reference ({e_bill_vendor_ref})")
                    .format(
                        bill_vendor_ref=bill.reference or "",
                        e_bill_vendor_ref=bill.e_invoice_reference
                    ))

            if (bill.e_invoice_date_invoice and
                    bill.e_invoice_date_invoice != bill.date_invoice):
                error_messages.append(
                    _("Invoice date ({bill_date_invoice}) "
                      "does not match with "
                      "e-bill invoice date ({e_bill_date_invoice})")
                    .format(
                        bill_date_invoice=bill.date_invoice or "",
                        e_bill_date_invoice=bill.e_invoice_date_invoice
                    ))

            if not error_messages:
                continue
            bill.e_invoice_validation_error = True
            bill.e_invoice_validation_message = \
                ",\n".join(error_messages) + "."

    @api.multi
    def name_get(self):
        result = super(AccountInvoice, self).name_get()
        res = []
        for tup in result:
            invoice = self.browse(tup[0])
            if invoice.type in ('in_invoice', 'in_refund'):
                name = "%s, %s" % (tup[1], invoice.partner_id.name)
                if invoice.amount_total_signed:
                    name += ', %s %s' % (
                        invoice.amount_total_signed, invoice.currency_id.symbol
                    )
                if invoice.origin:
                    name += ', %s' % invoice.origin
                res.append((invoice.id, name))
            else:
                res.append(tup)
        return res

    @api.multi
    def remove_attachment_link(self):
        self.ensure_one()
        self.fatturapa_attachment_in_id = False
        return {'type': 'ir.actions.client', 'tag': 'reload'}

    @api.model
    def compute_xml_amount_untaxed(self, DatiRiepilogo):
        amount_untaxed = 0.0
        for Riepilogo in DatiRiepilogo:
            rounding = float(Riepilogo.Arrotondamento or 0.0)
            amount_untaxed += float(Riepilogo.ImponibileImporto) + rounding
        return amount_untaxed

    @api.model
    def compute_xml_amount_tax(self, DatiRiepilogo):
        amount_tax = 0.0
        for Riepilogo in DatiRiepilogo:
            amount_tax += float(Riepilogo.Imposta)
        return amount_tax

    def set_einvoice_data(self, fattura):
        self.ensure_one()
        amount_untaxed = self.compute_xml_amount_untaxed(
            fattura.DatiBeniServizi.DatiRiepilogo)
        amount_tax = self.compute_xml_amount_tax(
            fattura.DatiBeniServizi.DatiRiepilogo)
        amount_total = float(
            fattura.DatiGenerali.DatiGeneraliDocumento.
            ImportoTotaleDocumento or 0.0)
        reference = fattura.DatiGenerali.DatiGeneraliDocumento.Numero
        date_invoice = fattura.DatiGenerali.DatiGeneraliDocumento.Data

        self.update({
            'e_invoice_amount_untaxed': amount_untaxed,
            'e_invoice_amount_tax': amount_tax,
            'e_invoice_amount_total': amount_total,
            'e_invoice_reference': reference,
            'e_invoice_date_invoice': date_invoice,
        })


class FatturapaArticleCode(models.Model):
    # _position = ['2.2.1.3']
    _name = "fatturapa.article.code"
    _description = 'E-bill Article Code'

    name = fields.Char('Code Type')
    code_val = fields.Char('Code Value')
    e_invoice_line_id = fields.Many2one(
        'einvoice.line', 'Related E-bill Line', readonly=True
    )


class AccountInvoiceLine(models.Model):
    # _position = [
    #     '2.2.1.3', '2.2.1.6', '2.2.1.7',
    #     '2.2.1.8', '2.1.1.10'
    # ]
    _inherit = "account.invoice.line"

    fatturapa_attachment_in_id = fields.Many2one(
        'fatturapa.attachment.in', 'E-bill Import File',
        readonly=True, related='invoice_id.fatturapa_attachment_in_id')


class DiscountRisePrice(models.Model):
    _inherit = "discount.rise.price"
    e_invoice_line_id = fields.Many2one(
        'einvoice.line', 'Related E-bill Line', readonly=True
    )


class EInvoiceLine(models.Model):
    _name = 'einvoice.line'
    invoice_id = fields.Many2one(
        "account.invoice", "Bill", readonly=True)
    line_number = fields.Integer('Line Number', readonly=True)
    service_type = fields.Char('Sale Provision Type', readonly=True)
    cod_article_ids = fields.One2many(
        'fatturapa.article.code', 'e_invoice_line_id',
        'Articles Code', readonly=True
    )
    name = fields.Char("Description", readonly=True)
    qty = fields.Float(
        "Quantity", readonly=True,
        digits=dp.get_precision('Product Unit of Measure')
    )
    uom = fields.Char("Unit of measure", readonly=True)
    period_start_date = fields.Date("Period Start Date", readonly=True)
    period_end_date = fields.Date("Period End Date", readonly=True)
    unit_price = fields.Float(
        "Unit Price", readonly=True,
        digits=dp.get_precision('Product Price')
    )
    discount_rise_price_ids = fields.One2many(
        'discount.rise.price', 'e_invoice_line_id',
        'Discount and Supplement Details', readonly=True
    )
    total_price = fields.Float("Total Price", readonly=True)
    tax_amount = fields.Float("VAT Rate", readonly=True)
    wt_amount = fields.Char("Tax Withholding", readonly=True)
    tax_kind = fields.Char("Nature", readonly=True)
    admin_ref = fields.Char("Administration Reference", readonly=True)
    other_data_ids = fields.One2many(
        "einvoice.line.other.data", "e_invoice_line_id",
        string="Other Administrative Data", readonly=True)


class EInvoiceLineOtherData(models.Model):
    _name = 'einvoice.line.other.data'

    e_invoice_line_id = fields.Many2one(
        'einvoice.line', 'Related E-bill Line', readonly=True
    )
    name = fields.Char("Data Type", readonly=True)
    text_ref = fields.Char("Text Reference", readonly=True)
    num_ref = fields.Float("Number Reference", readonly=True)
    date_ref = fields.Char("Date Reference", readonly=True)
