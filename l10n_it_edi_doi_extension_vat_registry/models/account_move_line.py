# Copyright 2026 Simone Rubino
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _l10n_it_edi_doi_ext_get_validation_message(self, doi_tax):
        message = super()._l10n_it_edi_doi_ext_get_validation_message(doi_tax)
        self.ensure_one()
        if message:
            not_allowed_extra_taxes = self._get_not_allowed_doi_extra_taxes(doi_tax)
            if not_allowed_extra_taxes:
                extra_message = self.env._(
                    "Only Taxes excluded from VAT Registries are allowed.\n"
                    "The Taxes %(taxes)s are not allowed.",
                    taxes=", ".join(not_allowed_extra_taxes.mapped("name")),
                )
                message = "\n".join((message, extra_message))
            else:
                message = ""
        return message

    def _get_not_allowed_doi_extra_taxes(self, doi_tax):
        """Taxes that are not allowed in a line containing the DoI Tax."""
        # Only taxes excluded from VAT Registries
        # can be in a line containing the DoI Tax
        extra_taxes = self.tax_ids - doi_tax
        not_allowed_extra_taxes = extra_taxes - extra_taxes.filtered(
            "exclude_from_registries"
        )
        return not_allowed_extra_taxes

    def _is_counted_for_doi(self, doi_tax):
        is_counted = super()._is_counted_for_doi(doi_tax)
        if not is_counted and doi_tax in self.tax_ids:
            not_allowed_extra_taxes = self._get_not_allowed_doi_extra_taxes(doi_tax)
            is_counted = not bool(not_allowed_extra_taxes)
        return is_counted
