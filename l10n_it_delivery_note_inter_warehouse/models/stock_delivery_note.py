# Copyright 2023 Ooops404
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockDeliveryNote(models.Model):
    _inherit = "stock.delivery.note"

    def update_detail_lines(self):
        res = super().update_detail_lines()
        for note in self:
            inter_wh_note_id = note.picking_ids[-1].mapped(
                "move_lines.inter_warehouse_picking_id.delivery_note_id"
            )
            if inter_wh_note_id:
                note.partner_ref = inter_wh_note_id.name
                note.write(
                    {
                        field: inter_wh_note_id[field]
                        for field in self._get_sync_fields()
                        if inter_wh_note_id[field]
                    }
                )
        return res
