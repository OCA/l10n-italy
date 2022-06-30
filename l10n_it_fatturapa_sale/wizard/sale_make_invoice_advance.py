# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        invoice = super()._create_invoice(order, so_line, amount)
        order = invoice.invoice_line_ids.mapped('sale_line_ids.order_id')
        sale_documents = order.mapped('related_documents')
        invoice.update({
            'related_documents': [
                (4, sale_document_id)
                for sale_document_id in sale_documents.ids],
        })
        return invoice
