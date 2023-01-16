# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.tools.misc import formatLang


class Company(models.Model):
    _inherit = "res.company"

    rea_office = fields.Many2one(
        "res.country.state",
        string="Office Province",
        related="partner_id.rea_office",
        store=True,
        readonly=False,
    )
    rea_code = fields.Char(
        "REA Code", size=20, related="partner_id.rea_code", store=True, readonly=False
    )
    rea_capital = fields.Float(
        "Share Capital", related="partner_id.rea_capital", store=True, readonly=False
    )
    rea_member_type = fields.Selection(
        related="partner_id.rea_member_type",
        readonly=False,
    )
    rea_liquidation_state = fields.Selection(
        related="partner_id.rea_liquidation_state",
        readonly=False,
    )

    @api.onchange(
        "rea_office",
        "rea_code",
        "rea_capital",
        "rea_member_type",
        "rea_liquidation_state",
    )
    def onchange_rea_data(self):
        if (
            self.rea_office
            or self.rea_code
            or self.rea_capital
            or self.rea_member_type
            or self.rea_liquidation_state
        ):
            rea_member_type = ""
            if self.rea_member_type:
                rea_member_type = dict(
                    self.env["res.partner"]
                    ._fields["rea_member_type"]
                    ._description_selection(self.env)
                )[self.rea_member_type]
            rea_liquidation_state = ""
            if self.rea_liquidation_state:
                rea_liquidation_state = dict(
                    self.env["res.partner"]
                    ._fields["rea_liquidation_state"]
                    ._description_selection(self.env)
                )[self.rea_liquidation_state]
            # using always €, as this is a registry of Italian companies
            company_registry = _(
                "%(rea_office.code)s - %(rea_code)s / "
                "Share Cap. %(rea_capital)s € / %(rea_member_type)s / %(rea_liquidation_state)s"
            ) % {
                "rea_office.code": self.rea_office.code or "",
                "rea_code": self.rea_code or "",
                "rea_capital": formatLang(self.env, self.rea_capital),
                "rea_member_type": rea_member_type,
                "rea_liquidation_state": rea_liquidation_state,
            }
            self.company_registry = company_registry
