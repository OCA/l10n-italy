# Copyright 2026 Simone Rubino
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _l10n_it_edi_doi_ext_get_validation_message(self, doi_tax):
        message = super()._l10n_it_edi_doi_ext_get_validation_message(doi_tax)
        self.ensure_one()
        if message:
            extra_taxes = self.tax_ids - doi_tax
            not_allowed_extra_taxes = extra_taxes - extra_taxes.filtered(
                "exclude_from_registries"
            )
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
