# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio
# Copyright 2016 Lorenzo Battistini - Agile Business Group
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class FatturaPAAttachment(models.Model):
    _name = "fatturapa.attachment.out"
    _description = "FatturaPA Export File"
    _inherits = {'ir.attachment': 'ir_attachment_id'}
    _inherit = ['mail.thread']

    ir_attachment_id = fields.Many2one(
        'ir.attachment', 'Attachment', required=True, ondelete="cascade")
    out_invoice_ids = fields.One2many(
        'account.invoice', 'fatturapa_attachment_out_id',
        string="Out Invoices", readonly=True)
