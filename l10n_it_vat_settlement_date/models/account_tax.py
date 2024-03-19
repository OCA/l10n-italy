# Copyright (c) 2021 Marco Colombo (https://github/TheMule71)
# Copyright 2024 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models
from odoo.osv import expression


class AccountTax(models.Model):
    _inherit = "account.tax"

    def _get_settlement_date_domain(self, domain):
        """Create a copy of `domain`
        where the settlement date is used instead of move date."""
        # Substitute `date` with the settlement date in domain terms
        settlement_domain = []
        for term in domain:
            if term[0] == "date":
                # 'tuple' object does not support item assignment
                # so we have to create another term with the new date
                term = "l10n_it_vat_settlement_date", *term[1:]
            settlement_domain.append(term)
        return settlement_domain

    def _inject_vat_settlement_date_domain(self, domain):
        """Create a new domain where the settlement date is used instead of move date.

        The domain falls back on the move date if the settlement date is empty.
        """
        settlement_domain = self._get_settlement_date_domain(domain)
        domain = expression.OR(
            [
                settlement_domain,
                expression.AND(
                    [
                        [("l10n_it_vat_settlement_date", "=", None)],
                        domain,
                    ]
                ),
            ]
        )
        return domain

    def get_move_line_partial_domain(self, from_date, to_date, company_ids):
        domain = super().get_move_line_partial_domain(from_date, to_date, company_ids)
        if self.env.context.get("use_l10n_it_vat_settlement_date"):
            domain = self._inject_vat_settlement_date_domain(domain)
        return domain
