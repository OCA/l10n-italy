# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    fiscalcode = fields.Char(
        related="partner_id.fiscalcode", store=True, readonly=False
    )
    l10n_it_fiscalcode_check_uniqueness = fields.Boolean(
        string="Fiscal code is unique",
        help="When the fiscal code of a partner is edited, raise an error "
        "if there is another partner with the same fiscal code.",
    )

    def l10n_it_fiscalcode_check_uniqueness_constraint(self):
        """Check the fiscal code of all the partners in `self`."""
        partners = self.env["res.partner"].search(
            [
                ("company_id", "in", [False] + self.ids),
            ]
        )
        partners._l10n_it_fiscalcode_constrain_uniqueness()
