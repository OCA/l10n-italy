#  Copyright 2021 Alfredo Zamora - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, api


class StockPickingPackagePreparation(models.Model):
    _inherit = "stock.picking.package.preparation"

    @api.multi
    def other_operations_on_ddt(self, invoice):
        """
        This method allows to create a proper kit invoicing.
        in case of bom in sale.order.line, will be:
        - created a section with product kit name
        - created a new invoice line based sale.order.line (product kit)
        - moved the invoice line of the kit component below the product kit invoice line
        """

        super(StockPickingPackagePreparation,
              self).other_operations_on_ddt(invoice)
        for ddt in self:
            sale_order_lines = ddt.line_ids.mapped('sale_line_id')
            for sale_order_line in sale_order_lines:
                bom = sale_order_line.get_mrp_bom()
                if bom:
                    bom_products = bom.bom_line_ids.mapped('product_id')
                    # get already created invoice_line_ids with bom_products
                    invoice_line_ids = invoice.invoice_line_ids.filtered(
                        lambda l: l.product_id in bom_products)
                    if invoice_line_ids:
                        # create invoice section
                        line_ids_len = len(invoice.invoice_line_ids)
                        sequence = invoice.invoice_line_ids[
                                       line_ids_len - 1].sequence + 1
                        self.env['account.invoice.line'].create({
                            'sequence': sequence,
                            'name': bom.product_tmpl_id.name,
                            'display_type': 'line_section',
                            'invoice_id': invoice.id
                        })
                        # create invoice line using sale_order_line (product kit)
                        sequence += 1
                        product_kit_line = sale_order_line.invoice_line_create(
                            invoice.id, sale_order_line.product_qty)
                        product_kit_line.sequence = sequence
                        for line in invoice_line_ids:
                            sequence += 1
                            # move invoice lines below line section
                            line.sequence = sequence


class StockPickingPackagePreparationLine(models.Model):
    _inherit = "stock.picking.package.preparation.line"

    @api.multi
    def _prepare_invoice_line(self, qty, invoice_id=None):
        """
        in case of mrp.bom from sale.order.line values will be updated to avoid
        invoicing
        """
        res = super(StockPickingPackagePreparationLine, self)._prepare_invoice_line(
            qty,
            invoice_id
        )

        mrp_bom = self.sale_line_id.get_mrp_bom()

        if mrp_bom:
            res.update({
                'price_unit': False,
                'discount': False,
                'invoice_line_tax_ids': False,
            })
        return res
