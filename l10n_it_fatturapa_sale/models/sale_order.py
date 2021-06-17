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
        groups="account.group_account_user",
    )

    @api.multi
    def _finalize_invoices(self, invoices, references):
        res = super()._finalize_invoices(invoices, references)
        # To each invoice, link the documents of the related order
        # only if the order is in `self`
        for invoice in invoices.values():
            orders = invoice.invoice_line_ids.mapped('sale_line_ids.order_id')
            orders = orders.filtered(lambda o: o in self)
            # Use sudo because current user might not be able to
            # read/write the related documents
            # but they should propagate to the invoice just the same
            orders_sudo = orders.sudo()
            sale_documents = orders_sudo.mapped('related_documents')
            invoice_sudo = invoice.sudo()
            invoice_sudo.update({
                'related_documents': [
                    (4, sale_document_id)
                    for sale_document_id in sale_documents.ids],
            })
        return res

    @api.multi
    def unlink(self):
        # Use sudo because current user might not be able to
        # read the related documents
        # but they should be unlinked just the same
        self_sudo = self.sudo()
        related_documents = self_sudo.mapped('related_documents')
        res = super().unlink()
        related_documents.check_unlink().unlink()
        return res
