from odoo import api, fields, models


class StockDeliveryNoteSelect(models.TransientModel):
    _inherit = "stock.delivery.note.select.wizard"

    is_inter_warehouse = fields.Boolean(compute="_compute_is_inter_warehouse")

    @api.depends("picking_ids.move_lines.inter_warehouse_picking_id")
    def _compute_is_inter_warehouse(self):
        for rec in self:
            rec.is_inter_warehouse = any(
                rec.picking_ids.mapped("move_lines.inter_warehouse_picking_id")
            )
