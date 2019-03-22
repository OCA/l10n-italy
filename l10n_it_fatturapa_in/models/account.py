
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.tools import float_compare
import odoo.addons.decimal_precision as dp


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
    e_invoice_validation_error = fields.Boolean(
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

    @api.depends('amount_untaxed', 'amount_tax', 'amount_total', 'state')
    def _compute_e_invoice_validation_error(self):
        for invoice in self:
            if (invoice.type in ['in_invoice', 'in_refund'] and
                    invoice.state in ['draft', 'open', 'paid'] and
                    invoice.fatturapa_attachment_in_id):
                if (invoice.e_invoice_amount_untaxed and
                        float_compare(invoice.amount_untaxed,
                                      invoice.e_invoice_amount_untaxed,
                                      precision_rounding=invoice.currency_id
                                      .rounding) != 0):
                    invoice.e_invoice_validation_error = True
                elif (invoice.e_invoice_amount_tax and
                        float_compare(invoice.amount_tax,
                                      invoice.e_invoice_amount_tax,
                                      precision_rounding=invoice.currency_id
                                      .rounding) != 0):
                    invoice.e_invoice_validation_error = True
                elif (invoice.e_invoice_amount_total and
                        float_compare(invoice.amount_total,
                                      invoice.e_invoice_amount_total,
                                      precision_rounding=invoice.currency_id
                                      .rounding) != 0):
                    invoice.e_invoice_validation_error = True
                else:
                    invoice.e_invoice_validation_error = False
            else:
                invoice.e_invoice_validation_error = False

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
            amount_untaxed += float(Riepilogo.ImponibileImporto)
        return amount_untaxed

    @api.model
    def compute_xml_amount_tax(self, DatiRiepilogo):
        amount_tax = 0.0
        for Riepilogo in DatiRiepilogo:
            amount_tax += float(Riepilogo.Imposta)
        return amount_tax

    def set_einvoice_amount(self, fattura):
        self.ensure_one()
        amount_untaxed = self.compute_xml_amount_untaxed(
            fattura.DatiBeniServizi.DatiRiepilogo)
        amount_tax = self.compute_xml_amount_tax(
            fattura.DatiBeniServizi.DatiRiepilogo)
        amount_total = float(
            fattura.DatiGenerali.DatiGeneraliDocumento.
            ImportoTotaleDocumento or 0.0)

        self.update({
            'e_invoice_amount_untaxed': amount_untaxed,
            'e_invoice_amount_tax': amount_tax,
            'e_invoice_amount_total': amount_total,
        })


class fatturapa_article_code(models.Model):
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
    _description = 'E-invoice line'
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
    _description = 'E-invoice line other data'

    e_invoice_line_id = fields.Many2one(
        'einvoice.line', 'Related E-bill Line', readonly=True
    )
    name = fields.Char("Data Type", readonly=True)
    text_ref = fields.Char("Text Reference", readonly=True)
    num_ref = fields.Float("Number Reference", readonly=True)
    date_ref = fields.Char("Date Reference", readonly=True)
