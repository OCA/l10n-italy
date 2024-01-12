# Copyright 2023 Ooops404
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockDeliveryNote(models.Model):
    _inherit = "stock.delivery.note"

    def update_detail_lines(self):
        res = super().update_detail_lines()
        for note in self:
            picking_ids = note.picking_ids.filtered("intercompany_picking_id")
            if picking_ids:
                # We want to give access to the referenced
                # delivery note only in this specific case
                intercompany_picking_id = fields.first(
                    picking_ids[::-1]
                ).intercompany_picking_id.sudo()

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
