# -*- coding: utf-8 -*-
# Copyright 2015 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api, _
from openerp.exceptions import Warning as UserError


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    @api.multi
    def invoice_validate(self):
        res = super(AccountInvoice, self).invoice_validate()
        for invoice in self:
            invoice_type = invoice.type
            if invoice_type in ('in_invoice', 'in_refund'):
                return res
            if self.search([('type', '=', invoice_type),
                            ('date_invoice', '>', invoice.date_invoice),
                            ('number', '<', invoice.number),
                            ('journal_id', '=', invoice.journal_id.id), ]):
                raise UserError(_(
                    'Cannot create invoice! Post the invoice with '
                    'a greater date'))
        return res
