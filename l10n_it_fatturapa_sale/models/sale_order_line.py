#  Copyright 2020 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    related_documents = fields.One2many(
        comodel_name='fatturapa.related_document_type',
        inverse_name='sale_order_line_id',
        string='Related Documents',
        copy=False,
        groups="account.group_account_user,sales_team.group_sale_salesman",
    )
    admin_ref = fields.Char(
        string="Admin. ref.",
        size=20,
        copy=False,
        groups="account.group_account_user,sales_team.group_sale_salesman",
    )

    @api.multi
    def _prepare_invoice_line(self, qty):
        self.ensure_one()
        invoice_line_vals = super()._prepare_invoice_line(qty)
        sale_line_documents = self.related_documents
        if sale_line_documents:
            invoice_line_documents = invoice_line_vals.get(
                'related_documents', list())
            invoice_line_documents.extend(
                (4, line_document_id)
                for line_document_id in sale_line_documents.ids)
            invoice_line_vals.update({
                'related_documents': invoice_line_documents,
            })

        sale_line_admin_ref = self.admin_ref
        if sale_line_admin_ref:
            invoice_line_admin_ref = invoice_line_vals.get('admin_ref')
            invoice_line_admin_ref = ', '.join(filter(None, [
                invoice_line_admin_ref,
                sale_line_admin_ref,
            ]))
            invoice_line_vals.update({
                'admin_ref': invoice_line_admin_ref,
            })
        return invoice_line_vals

    @api.multi
    def unlink(self):
        related_documents = self.mapped('related_documents')
        res = super().unlink()
        related_documents.check_unlink().unlink()
        return res
