#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    l10n_it_fiscalcode_check_uniqueness = fields.Boolean(
        related="company_id.l10n_it_fiscalcode_check_uniqueness",
        readonly=False,
    )

    def l10n_it_fiscalcode_check_uniqueness_constraint(self):
        """Check the fiscal code of all the partners in current company."""
        self.company_id.l10n_it_fiscalcode_check_uniqueness_constraint()
