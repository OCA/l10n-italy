# Copyright 2026 Simone Rubino
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _l10n_it_edi_doi_ext_get_validation_message(self, doi_tax):
        """
        Message explaining why this line is not accepted in a Move linked to a DoI.
        """
        self.ensure_one()
        return (
            self.env._(
                "Since the invoice line %(line_name)s includes "
                "the Tax %(doi_tax)s for the Declaration of Intent, it cannot include "
                "other Taxes.",
                doi_tax=doi_tax.name,
                line_name=self.name,
            )
            # Lines having only taxes different from the DoI Tax are accepted
            # in order to support mixed Moves
            if doi_tax in self.tax_ids and not self._is_counted_for_doi(doi_tax)
            else ""
        )

    def _is_counted_for_doi(self, doi_tax):
        """True only if this line counts for the DoI total of the Move."""
        return doi_tax in self.tax_ids and self.tax_ids == doi_tax
