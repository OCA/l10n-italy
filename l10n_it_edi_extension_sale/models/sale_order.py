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

    def _create_account_invoices(self, invoice_vals_list, final):
        for invoice_vals in invoice_vals_list:
            id_sale_lines = [
                invoice_line[-1]["sale_line_ids"][0][1]
                for invoice_line in invoice_vals["invoice_line_ids"]
            ]

            sale_order_lines = self.env["sale.order.line"].browse(id_sale_lines)
            sale_orders = sale_order_lines.mapped("order_id")

            invoice_vals["related_document_ids"] = [
                Command.link(rd.id) for rd in sale_orders.related_document_ids
            ]
        return super()._create_account_invoices(invoice_vals_list, final)

    def unlink(self):
        related_documents = self.mapped("related_document_ids")
        res = super().unlink()
        related_documents.check_unlink().unlink()
        return res
