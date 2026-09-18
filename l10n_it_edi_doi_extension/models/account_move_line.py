# Copyright 2026 Simone Rubino
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _l10n_it_edi_doi_ext_get_validation_message(self, doi_tax):
        """Message explaining why this line is not counted for the DoI of the Move."""
        self.ensure_one()
        return (
            self.env._(
                "The invoice line %(line_name)s must "
                "include only the Tax %(doi_tax)s for the Declaration of Intent.",
                doi_tax=doi_tax.name,
                line_name=self.name,
            )
            # The line only contains the DoI Tax
            if not (self.tax_ids == doi_tax)
            else ""
        )
