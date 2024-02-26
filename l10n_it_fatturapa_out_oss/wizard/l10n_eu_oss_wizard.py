from odoo import models


class L10nEuOssWizard(models.TransientModel):
    _inherit = "l10n.eu.oss.wizard"

    def _prepare_tax_vals(self, country, tax, rate, tax_group):
        vals = super()._prepare_tax_vals(country, tax, rate, tax_group)
        vals["kind_id"] = self.env.ref("l10n_it_account_tax_kind.n3_2").id
        return vals
