# Copyright 2023 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _create_invoice(self, order, so_line, amount):
        invoice = super()._create_invoice(order, so_line, amount)
        if (
            self.advance_payment_method in ("fixed", "percentage")
            and invoice.journal_id.advance_fiscal_document_type_id
        ):
            invoice.fiscal_document_type_id = (
                invoice.journal_id.advance_fiscal_document_type_id
            )
        return invoice
