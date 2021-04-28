from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    vsc_supply_code = fields.Char(
        "Vat statement communication supply code",
        default="IVP18",
        help="IVP18",
    )
