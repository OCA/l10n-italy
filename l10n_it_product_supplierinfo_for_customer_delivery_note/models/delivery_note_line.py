# Copyright 2016 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class StockDeliveryNoteLine(models.Model):

    _inherit = "stock.delivery.note.line"
    product_customer_code = fields.Char(
        "Product Customer Code", compute="_compute_customer_code"
    )

    product_customer_name = fields.Char(
        "Product Customer Name", compute="_compute_customer_name"
    )

    def _compute_customer_code(self):
        for line in self:
            line.product_customer_code = line.product_id.default_code
            if line.move_id and line.move_id.product_customer_code:
                line.product_customer_code = line.move_id.product_customer_code

    def _compute_customer_name(self):
        for line in self:
            line.product_customer_name = line.product_id.name
            if line.move_id and line.move_id.product_customer_name:
                line.product_customer_name = line.move_id.product_customer_name
