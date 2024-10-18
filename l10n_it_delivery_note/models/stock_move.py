from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def write(self, vals):
        res = super().write(vals)
        delivery_note_ids = self.mapped("picking_id.delivery_note_id")
        if delivery_note_ids and self.quantity_done:
            delivery_note_ids.with_context(
                force_update_detail_lines=True
            ).update_detail_lines()

        return res
