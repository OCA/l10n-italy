# -*- coding: utf-8 -*-
# Copyright 2017 Andrea Cometa - Apulia Software
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class StockPickingPackagePreparation(models.Model):

    _inherit = 'stock.picking.package.preparation'
    _rec_name = 'display_name'

    @api.multi
    def action_put_in_pack(self):
        # we add a the shipping cost
        for cost in self.company_id.shipment_cost_ids:
            if cost.lower_limit < self.amount_untaxed < cost.upper_limit:
                self.env['stock.picking.package.preparation.line'].create({
                    'package_preparation_id': self.id,
                    'product_id': cost.shipment_cost_product_id.id,
                    'product_uom_qty': 1.0,
                    'product_uom': cost.shipment_cost_product_id.uom_id.id,
                    'name': cost.shipment_cost_product_id.name,
                })
        return super(StockPickingPackagePreparation, self).action_put_in_pack()
