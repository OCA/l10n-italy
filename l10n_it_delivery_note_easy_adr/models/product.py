from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_adr = fields.Boolean(string="is Adr Product", default=False)
    adr_category_id = fields.Many2one(
        string="ADR Category", comodel_name="product.adr.category"
    )
    adr_text = fields.Text(string="Adr Text")
    adr_weight = fields.Selection(
        string="Weight field",
        selection=[("weight", "Weight"), ("qty", "Quantity")],
        default="qty",
    )
