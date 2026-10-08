#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import models


class AccountVatPeriodEndStatement(models.Model):
    _inherit = "account.vat.period.end.statement"

    def compute_amounts(self):
        return super(
            AccountVatPeriodEndStatement,
            self.with_context(
                use_l10n_it_vat_settlement_date=True,
            ),
        ).compute_amounts()
