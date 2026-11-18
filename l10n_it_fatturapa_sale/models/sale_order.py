#  Copyright 2020 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    related_documents = fields.One2many(
        comodel_name="fatturapa.related_document_type",
        inverse_name="sale_order_id",
        copy=False,
        groups="account.group_account_user,sales_team.group_sale_salesman",
    )

    def _create_invoices(self, grouped=False, final=False, date=None):
        moves = super()._create_invoices(grouped=grouped, final=final, date=date)

        # To each invoice, link the documents of the related order
        # only if the order is in `self`
        for invoice in moves:
            orders = invoice.invoice_line_ids.mapped("sale_line_ids.order_id")
            orders = orders.filtered(lambda o: o in self)
            sale_documents = orders.mapped("related_documents")
            invoice.update(
                {
                    "related_documents": [
                        (4, sale_document_id) for sale_document_id in sale_documents.ids
                    ],
                }
            )
        return moves

    def unlink(self):
        related_documents = self.mapped("related_documents")
        res = super().unlink()
        related_documents.check_unlink().unlink()
        return res

    def _prepare_invoice(self):
        """
        English:
        When creating an invoice from a sale order, if the payment method
        is RiBa (MP12),the recipient bank is automatically removed. This
        ensures that the customer invoice is issued without a recipient bank,
        as the recipient bank for RiBa is decided at a later stage. This avoids
        misleading the customer and prevents potential disputes.
        """
        res = super()._prepare_invoice()
        payment_term = self.env["account.payment.term"]
        payment_mode = payment_term.browse(
            res["invoice_payment_term_id"]
        ).fatturapa_pm_id.code
        if res.get("partner_bank_id") and payment_mode == "MP12":
            res["partner_bank_id"] = False
        return res
