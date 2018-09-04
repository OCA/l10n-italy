# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    fatturapa_attachment_in_id = fields.Many2one(
        'fatturapa.attachment.in', 'E-Invoice Import File',
        ondelete='restrict')
    inconsistencies = fields.Text('Import Inconsistencies')


class fatturapa_article_code(models.Model):
    # _position = ['2.2.1.3']
    _name = "fatturapa.article.code"
    _description = 'FatturaPA Article Code'

    name = fields.Char('Cod Type')
    code_val = fields.Char('Code Value')
    invoice_line_id = fields.Many2one(
        'account.invoice.line', 'Related Invoice line',
        ondelete='cascade', index=True
    )


class account_invoice_line(models.Model):
    # _position = [
    #     '2.2.1.3', '2.2.1.6', '2.2.1.7',
    #     '2.2.1.8', '2.1.1.10'
    # ]
    _inherit = "account.invoice.line"

    cod_article_ids = fields.One2many(
        'fatturapa.article.code', 'invoice_line_id',
        'Cod. Articles'
    )
    service_type = fields.Selection([
        ('SC', 'sconto'),
        ('PR', 'premio'),
        ('AB', 'abbuono'),
        ('AC', 'spesa accessoria'),
        ], string="Service Type")
    ftpa_uom = fields.Char('Fattura Pa Unit of Measure')
    service_start = fields.Date('Service start at')
    service_end = fields.Date('Service end at')
    discount_rise_price_ids = fields.One2many(
        'discount.rise.price', 'invoice_line_id',
        'Discount and Rise Price Details'
    )
