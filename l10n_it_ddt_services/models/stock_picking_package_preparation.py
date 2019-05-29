# -*- coding: utf-8 -*-


from odoo import fields, models, api, _


class StockPickingPackagePreparation(models.Model):
    _inherit = "stock.picking.package.preparation"

    @api.multi
    def other_operations_on_ddt(self, invoice):
        """
        Once invoices are created with stockable products, we add them
        all the invoiceable services available in the SO related to the
        DDTs linked to the invoice
        """
        for ddt in self:
            super(StockPickingPackagePreparation,
                  ddt).other_operations_on_ddt(invoice)
            order_ids = ddt.line_ids.mapped('sale_line_id.order_id').filtered(
                lambda o: not o.ddt_invoice_exclude)
            line_ids = order_ids.order_line.filtered(
                lambda l: l.qty_to_invoice > 0 and
                l.product_id.type == 'service' and
                not l.product_id.ddt_invoice_exclude)

            # we call the Sale method for creating invoice
            for line in line_ids:
                qty = line.qty_to_invoice
                line.invoice_line_create(invoice.id, qty)
