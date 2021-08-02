# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


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

    @api.constrains("rea_office", "rea_code", "company_id")
    def constrain_rea_code(self):
        for partner in self:
            if not partner.rea_office or not partner.rea_code:
                continue
            rea_domain = [
                ("rea_office", "=", partner.rea_office.id),
                ("rea_code", "=", partner.rea_code),
                ("company_id", "=", partner.company_id.id),
                ("id", "!=", partner.id),
            ]
            other_rea_partners = self.search(rea_domain)
            if other_rea_partners:
                raise ValidationError(
                    _(
                        "The REA Code and Office Province must "
                        "be unique per company.\n"
                        "Please edit '{this_partner}' "
                        "or '{other_partners}' and try again."
                    ).format(
                        this_partner=partner.display_name,
                        other_partners=", ".join(
                            other_rea_partners.mapped("display_name")
                        ),
                    )
                )
