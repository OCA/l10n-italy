#  Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class L10nEuOssWizardInherit(models.TransientModel):
    _inherit = "l10n.eu.oss.wizard"

    def _prepare_tax_vals(self, country_id, tax_id, rate, tax_group):
        vals = super()._prepare_tax_vals(country_id, tax_id, rate, tax_group)
        vals["l10n_it_exempt_reason"] = "N3.2"
        return vals
