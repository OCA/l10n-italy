# Copyright (c) 2020 Marco Colombo
# @author: Marco Colombo <marco.colombo@gmail.com>

from odoo import fields, models


class StockDeliveryNote(models.Model):
    _inherit = 'stock.delivery.note'

    stock_picking_batch_id = \
        fields.Many2one('stock.picking.batch',
                        oldname="parent_stock_picking_batch_id",
                        string="Batch Picking",
                        readonly=True)
