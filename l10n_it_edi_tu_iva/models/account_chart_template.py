# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountChartTemplate(models.AbstractModel):
    _inherit = "account.chart.template"

    def _post_load_data(self, template_code, company, template_data):
        # The Italian chart of accounts ships the references of the repealed
        # VAT decrees: they are moved to the Testo Unico IVA as soon as the
        # chart is loaded, also on a database where the module is installed
        # before the company gets its chart.
        res = super()._post_load_data(template_code, company, template_data)
        if template_code == "it":
            company = company or self.env.company
            tax_model = self.env["account.tax"].with_context(active_test=False)
            taxes = tax_model.search(
                [
                    *tax_model._check_company_domain(company),
                    ("l10n_it_law_reference", "!=", False),
                ]
            )
            self.env["account.tax"]._l10n_it_tu_iva_update_law_references(taxes)
        return res
