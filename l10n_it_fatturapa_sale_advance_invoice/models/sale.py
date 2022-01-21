# Copyright 2022 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        invoice = super(SaleAdvancePaymentInv, self)._create_invoice(
            order, so_line, amount)
        if self.advance_payment_method in ('fixed', 'percentage') and \
                invoice.journal_id.advance_fiscal_document_type_id:
            invoice.fiscal_document_type_id = invoice.journal_id.\
                advance_fiscal_document_type_id
        return invoice
