# Copyright 2026 Lorenzo Battistini
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models

from .. import OSS_EXEMPT_REASON, OSS_LAW_REFERENCE


class L10nEuOssWizard(models.TransientModel):
    _inherit = "l10n.eu.oss.wizard"

    def _prepare_tax_vals(self, country_id, tax_id, rate, tax_group):
        vals = super()._prepare_tax_vals(country_id, tax_id, rate, tax_group)
        if self.company_id.account_fiscal_country_id.code == "IT":
            vals["l10n_it_exempt_reason"] = OSS_EXEMPT_REASON
            vals["l10n_it_law_reference"] = OSS_LAW_REFERENCE
        return vals
