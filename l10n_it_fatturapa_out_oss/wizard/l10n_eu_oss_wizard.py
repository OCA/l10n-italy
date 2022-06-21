from odoo import models


class L10nEuOssWizard(models.TransientModel):
    _inherit = "l10n.eu.oss.wizard"

    def _prepare_tax_vals(self, country_id, tax_id, rate):
        vals = super(L10nEuOssWizard, self)._prepare_tax_vals(country_id, tax_id, rate)
        vals["kind_id"] = self.env.ref("l10n_it_account_tax_kind.n3_2").id
        return vals
