# Copyright 2023 Ooops404
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockDeliveryNoteSelect(models.TransientModel):
    _inherit = "stock.delivery.note.select.wizard"

    is_inter_company = fields.Boolean(compute="_compute_is_inter_company")

    @api.depends("picking_ids.intercompany_picking_id")
    def _compute_is_inter_company(self):
        for rec in self:
            rec.is_inter_company = any(
                rec.picking_ids.mapped("intercompany_picking_id")
            )
