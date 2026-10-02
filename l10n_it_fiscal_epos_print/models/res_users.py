from odoo import fields, models


class ResUsersInherit(models.Model):
    _inherit = "res.users"

    fiscal_operator_number = fields.Char(
        string="Fiscal Printer Operator", size=1, default="1"
    )
