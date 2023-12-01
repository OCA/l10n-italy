# Copyright 2023 Ooops404
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models


class StockDeliveryNote(models.Model):
    _inherit = "stock.delivery.note"

    @api.model
    def _get_sync_fields(self):
        return [
            "date",
            "transport_datetime",
            "transport_condition_id",
            "goods_appearance_id",
            "transport_reason_id",
            "transport_method_id",
            "gross_weight",
            "net_weight",
            "packages",
            "volume",
        ]

    def update_detail_lines(self):
        res = super().update_detail_lines()
        all_pickings_ids = self.env["stock.picking"].search(
            [("delivery_note_id", "!=", False)]
        )
        for note in self:
            intercompany_picking_id = all_pickings_ids.filtered(
                lambda x: x.delivery_note_id.id == note.id and x.intercompany_picking_id
            ).intercompany_picking_id
            if intercompany_picking_id:
                # We want to give access to the referenced
                # delivery note only in this specific case
                intercompany_picking_id = intercompany_picking_id.sudo()

                intercompany_note = intercompany_picking_id.delivery_note_id
                note.partner_ref = intercompany_note.name

                note.write(
                    {
                        field: intercompany_note[field]
                        for field in self._get_sync_fields()
                        if intercompany_note[field]
                    }
                )

        return res
