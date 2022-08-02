from odoo import fields, models, _

class ADR(models.Model):
    _name = "product.adr.category"
    _description = "ADR"
    
    name = fields.Char(
        string="Name"
    )
    multiplier = fields.Integer(
        string="Multiplier"
    )
    active = fields.Boolean(
        string="Active",
        default=True
    )
