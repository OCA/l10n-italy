from odoo import fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    prevent_dn_create = fields.Boolean("Prevent DN's Create")
