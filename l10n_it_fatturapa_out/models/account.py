# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio
# Copyright 2016 Lorenzo Battistini - Agile Business Group
# Copyright 2018 Gianmarco Conte, Marco Calcagni - Dinamiche Aziendali srl
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from openerp import fields, models, api, _
from openerp.exceptions import Warning as UserError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    fatturapa_attachment_out_id = fields.Many2one(
        'fatturapa.attachment.out', 'FatturaPA Export File',
        readonly=True, copy=False)

    has_pdf_invoice_print = fields.Boolean(
        related='fatturapa_attachment_out_id.has_pdf_invoice_print',
        readonly=True)

    def preventive_checks(self):
        # hook for preventive checks. Override and raise exception, in case
        return

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
