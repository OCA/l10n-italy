#  Copyright 2020 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrder (models.Model):
    _inherit = 'sale.order'

    related_documents = fields.One2many(
        comodel_name='fatturapa.related_document_type',
        inverse_name='sale_order_id',
        string='Related Documents',
        copy=False,
        groups="account.group_account_user,sales_team.group_sale_salesman",
    )

    @api.multi
    def _finalize_invoices(self, invoices, references):
        res = super()._finalize_invoices(invoices, references)
        # To each invoice, link the documents of the related order
        # only if the order is in `self`
        for invoice in invoices.values():
            orders = invoice.invoice_line_ids.mapped('sale_line_ids.order_id')
            orders = orders.filtered(lambda o: o in self)
            sale_documents = orders.mapped('related_documents')
            invoice.update({
                'related_documents': [
                    (4, sale_document_id)
                    for sale_document_id in sale_documents.ids],
            })
        return res

    @api.multi
    def unlink(self):
        related_documents = self.mapped('related_documents')
        res = super().unlink()
        related_documents.check_unlink().unlink()
        return res
