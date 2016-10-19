# -*- coding: utf-8 -*-
# Copyright (C) 2014 Davide Corio
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.osv import fields, orm


class FatturaPAAttachment(orm.Model):
    _name = "fatturapa.attachment.out"
    _description = "FatturaPA Export File"
    _inherits = {'ir.attachment': 'ir_attachment_id'}
    _inherit = ['mail.thread']

    _columns = {
        'ir_attachment_id': fields.many2one(
            'ir.attachment', 'Attachment', required=True, ondelete="cascade"),
        'out_invoice_ids': fields.one2many(
            'account.invoice', 'fatturapa_attachment_out_id',
            string="Out Invoices", readonly=True),
    }
