# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountTax(models.Model):
    _inherit = "account.tax"

    l10n_it_tu_iva_law_reference = fields.Char(
        string="TU IVA Law Reference",
        size=100,
        help="Normative reference to cite on the documents dated from the "
        "date the Testo Unico IVA applies (1 January 2027). It "
        "replaces the law reference of this tax and the wording that the "
        "module derives from the exoneration code, so it allows the taxes "
        "created by the user to cite the Testo Unico IVA too. Leave it "
        "empty to keep the automatic wording.",
    )

    @api.constrains("l10n_it_tu_iva_law_reference")
    def _check_l10n_it_tu_iva_law_reference(self):
        # The reference is written in the e-invoice as latin-1: any other
        # character is silently replaced by a question mark, so refuse it.
        for tax in self:
            reference = tax.l10n_it_tu_iva_law_reference
            if not reference:
                continue
            try:
                reference.encode("latin-1")
            except UnicodeEncodeError as error:
                raise ValidationError(
                    _(
                        "The Testo Unico IVA reference of the tax %(tax)s "
                        "contains characters that the electronic invoice "
                        "cannot contain: use latin-1 characters only.",
                        tax=tax.display_name,
                    )
                ) from error
