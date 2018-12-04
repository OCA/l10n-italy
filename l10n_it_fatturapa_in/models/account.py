# -*- coding: utf-8 -*-

from odoo import fields, models, api
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
