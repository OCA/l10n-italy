#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.tools import float_is_zero


class StockPickingPackagePreparation(models.Model):
    _inherit = "stock.picking.package.preparation"

    @api.multi
    def other_operations_on_ddt(self, invoice):
        """ Override this method to allow for proper kit invoicing.
        """
        super().other_operations_on_ddt(invoice)
        precision = self.env['decimal.precision'] \
            .precision_get('Product Unit of Measure')
        for ddt in self:
            kit_sale_lines = self.env['sale.order.line'].browse()
            bom_model = self.env['mrp.bom']
            for sale_line in ddt.line_ids.mapped('sale_line_id'):
                if not float_is_zero(
                    sale_line.qty_to_invoice,
                    precision_digits=precision,
                ):
                    bom = bom_model \
                        ._bom_find(
                            product=sale_line.product_id,
                        ) \
                        or bom_model.browse()
                    if bom.type == 'phantom':
                        kit_sale_lines |= sale_line

            # we call the Sale method for creating invoice lines
            for line in kit_sale_lines:
                qty = line.qty_to_invoice
                line.invoice_line_create(invoice.id, qty)
