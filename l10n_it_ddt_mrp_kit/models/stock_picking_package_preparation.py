# -*- coding: utf-8 -*-

from odoo import models, api
from odoo.tools import float_is_zero


class StockPickingPackagePreparation(models.Model):
    _inherit = "stock.picking.package.preparation"

    @api.multi
    def other_operations_on_ddt(self, invoice):
        """ Override this method to allow for proper kit invoicing.
        """
        def product_is_kit(line):
            return self.env['mrp.bom']._bom_find(
                product=line.product_id,
                company_id=line.company_id.id)

        super(StockPickingPackagePreparation,
              self).other_operations_on_ddt(invoice)
        precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        for ddt in self:
            line_ids = ddt.line_ids.mapped('sale_line_id').filtered(
                lambda l: not float_is_zero(
                    l.qty_to_invoice, precision_digits=precision)
                and product_is_kit(l))

            # we call the Sale method for creating invoice lines
            for line in line_ids:
                qty = line.qty_to_invoice
                line.invoice_line_create(invoice.id, qty)


class StockPickingPackagePreparationLine(models.Model):
    _inherit = "stock.picking.package.preparation.line"

    @api.multi
    def allow_invoice_line(self):
        self.ensure_one()
        res = super(StockPickingPackagePreparationLine,
                    self).allow_invoice_line()
        bom = self.env['mrp.bom']._bom_find(
            product=self.sale_line_id.product_id,
            company_id=self.package_preparation_id.company_id.id)

        return res and (not bom or bom.type != 'phantom')
