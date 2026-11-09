# Copyright 2026 Lorenzo Battistini
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models

from ..constants import OSS_EXEMPT_REASON, OSS_LAW_REFERENCE


class ResCompany(models.Model):
    _inherit = "res.company"

    def _get_country_specific_account_tax_fields(self):
        vals = super()._get_country_specific_account_tax_fields()
        if self.account_fiscal_country_id.code == "IT":
            vals["l10n_it_exempt_reason"] = OSS_EXEMPT_REASON
            vals["l10n_it_law_reference"] = OSS_LAW_REFERENCE
        return vals
