# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio
# Copyright 2016 Lorenzo Battistini - Agile Business Group
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class FatturaPAAttachment(models.Model):
    _name = "fatturapa.attachment.out"
    _description = "FatturaPA Export File"
    _inherits = {'ir.attachment': 'ir_attachment_id'}
    _inherit = ['mail.thread']
    _order = 'id desc'

    ir_attachment_id = fields.Many2one(
        'ir.attachment', 'Attachment', required=True, ondelete="cascade")
    out_invoice_ids = fields.One2many(
        'account.invoice', 'fatturapa_attachment_out_id',
        string="Out Invoices", readonly=True)
    has_pdf_invoice_print = fields.Boolean(
        help="True if all the invoices have a printed "
             "report attached in the XML, False otherwise.",
        compute='_compute_has_pdf_invoice_print', store=True)

    @api.multi
    @api.depends(
        'out_invoice_ids.fatturapa_doc_attachments.is_pdf_invoice_print')
    def _compute_has_pdf_invoice_print(self):
        """Check if all the invoices related to this attachment
        have at least one attachment containing
        the PDF report of the invoice"""
        for attachment_out in self:
            for invoice in attachment_out.out_invoice_ids:
                invoice_attachments = invoice.fatturapa_doc_attachments
                if any([ia.is_pdf_invoice_print
                        for ia in invoice_attachments]):
                    continue
                else:
                    attachment_out.has_pdf_invoice_print = False
                    break
            else:
                # We have examined all the invoices and none of them
                # has caused a break, this means all the invoices have at least
                # one attachment having is_pdf_invoice_print = True
                attachment_out.has_pdf_invoice_print = True


class FatturaAttachments(models.Model):
    _inherit = "fatturapa.attachments"

    is_pdf_invoice_print = fields.Boolean(
        help="This attachment contains the PDF report of the linked invoice")
