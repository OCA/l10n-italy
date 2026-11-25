# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
from odoo.fields import Command


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    related_document_ids = fields.One2many(
        "account.move.related_document",
        "sale_order_id",
        string="Related Documents",
        copy=False,
        groups="account.group_account_user,sales_team.group_sale_salesman",
    )

    def _create_invoices(self, grouped=False, final=False, date=None):
        moves = super()._create_invoices(grouped=grouped, final=final, date=date)

        # To each invoice, copy the documents of the related orders
        # only if the order is in `self`
        for invoice in moves:
            orders = invoice.invoice_line_ids.mapped("sale_line_ids.order_id")
            orders = orders.filtered(lambda o: o in self)
            sale_documents = orders.mapped("related_document_ids")
            if sale_documents:
                invoice.write(
                    {
                        "related_document_ids": [
                            Command.create(document_vals)
                            for document_vals in (
                                sale_documents._prepare_invoice_related_document_vals()
                            )
                        ],
                    }
                )
        return moves

    def unlink(self):
        # Order lines are deleted by the database (cascade),
        # so their documents have to be checked here too
        related_documents = self.mapped("related_document_ids") | self.mapped(
            "order_line.related_document_ids"
        )
        res = super().unlink()
        related_documents.check_unlink().unlink()
        return res
