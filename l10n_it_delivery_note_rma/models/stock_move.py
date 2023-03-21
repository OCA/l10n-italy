from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    delivery_note_line_id = fields.Many2one(
        "stock.delivery.note.line", "Delivery Line", index=True
    )
