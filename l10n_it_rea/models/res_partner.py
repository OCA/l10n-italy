# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    rea_office = fields.Many2one("res.country.state", string="Office Province")
    rea_code = fields.Char("REA Code", size=20)
    rea_capital = fields.Float("Share Capital")
    rea_member_type = fields.Selection(
        [("SU", "Unique Member"), ("SM", "Multiple Members")], "Member Type"
    )
    rea_liquidation_state = fields.Selection(
        [("LS", "In liquidation"), ("LN", "Not in liquidation")], "Liquidation State"
    )

    _sql_constraints = [
        (
            "rea_code_uniq",
            "unique (rea_office, rea_code, company_id)",
            "The rea code code must be unique per company !",
        ),
    ]
