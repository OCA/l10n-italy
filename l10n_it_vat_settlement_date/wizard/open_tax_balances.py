# Copyright 2025 Simone Rubino
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class WizardOpenTaxBalances(models.TransientModel):
    _inherit = "wizard.open.tax.balances"

    def open_taxes(self):
        action = super().open_taxes()
        action.setdefault("context", dict())["use_l10n_it_vat_settlement_date"] = True
        return action
