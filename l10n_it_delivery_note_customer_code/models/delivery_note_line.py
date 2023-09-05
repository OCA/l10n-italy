# Copyright 2016 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class StockDeliveryNoteLine(models.Model):

    _inherit = "stock.delivery.note.line"
    product_customer_code = fields.Char(
        string="Product Customer Code", related="move_id.product_customer_code"
    )

    product_customer_name = fields.Char(
        string="Product Customer Name", related="move_id.product_customer_name"
    )
