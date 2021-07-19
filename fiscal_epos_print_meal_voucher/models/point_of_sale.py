from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    ticket_credit_product_id = fields.Many2one(
        "product.product", string="Ticket credit product",
        domain="[('available_in_pos', '=', True), ('sale_ok', '=', True), "
               "('meal_voucher_ok', '=', True)]",
        help="Product used when issuing credit instead of giving change "
             "after receiving meal vouchers")
