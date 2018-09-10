# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio
# Copyright 2016 Lorenzo Battistini - Agile Business Group
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.tools.translate import _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    fatturapa_attachment_out_id = fields.Many2one(
        'fatturapa.attachment.out', 'FatturaPA Export File',
        readonly=True, copy=False)

    def preventive_checks(self):
        for line in self.invoice_line_ids:
            if '\n' in line.name:
                raise UserError(_(
                    "Invoice line [%s] must not contain new line character"
                ) % line.name)

    @api.multi
    def action_invoice_cancel(self):
        for invoice in self:
            if invoice.fatturapa_attachment_out_id:
                raise UserError(_(
                    "Invoice %s has XML and can't be canceled. "
                    "Delete the XML before"
                ) % invoice.number)
        res = super(AccountInvoice, self).action_invoice_cancel()
        return res
