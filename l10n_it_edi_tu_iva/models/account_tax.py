# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import re

from odoo import api, fields, models

#: Decrees replaced by the Testo Unico IVA: a reference citing one of them is
#: the only one this module updates, so a reference already changed by the user
#: is kept.
REPEALED_DECREE_RE = re.compile(r"\b(?:633|331|41)/\d")

#: Reference to cite in ``RiferimentoNormativo`` for each exoneration code,
#: mapped from the D.P.R. 633/1972 to the Testo Unico IVA. The articles are
#: transcribed from the Testo Unico and cross-checked against the published
#: article-by-article cross-reference tables of the reform.
#:
#: The values must stay within the limits enforced by ``l10n_it_edi`` when it
#: writes the element: at most 100 characters and latin-1 encodable (anything
#: else is replaced by ``?``), so the short "Art. X, c. Y" form is used, without
#: the en dash of the official wordings.
#:
#: ``N2.2`` is missing on purpose: the article depends on the operation
#: (art. 5, c. 3, art. 22, art. 139, art. 150, art. 157 ...), so the user sets
#: the article of each operation in the law reference of the tax.
#: ``N6.5``, ``N6.6`` and ``N6.8`` are missing too: since art. 64, c. 8,
#: D.Lgs. 10/2026 they no longer apply to operations carried out from 2027, so
#: those taxes have to be archived rather than given a new reference.
TU_IVA_REFERENCES = {
    "N1": "Art. 29, c. 1, D.Lgs. 10/2026",
    "N2.1": "Art. 17, D.Lgs. 10/2026",
    "N3.1": "Art. 45, c. 1, D.Lgs. 10/2026",
    "N3.2": "Art. 39, c. 1, lett. a), D.Lgs. 10/2026",
    "N3.3": "Art. 50, c. 1, D.Lgs. 10/2026",
    "N3.4": "Art. 48, c. 1, D.Lgs. 10/2026",
    "N3.5": "Art. 45, c. 1, lett. d), D.Lgs. 10/2026",
    "N3.6": "Art. 53, c. 5, D.Lgs. 10/2026",
    "N4": "Art. 37, c. 1, D.Lgs. 10/2026",
    "N5": "Art. 143, D.Lgs. 10/2026",
    "N6.1": "Art. 139, cc. 7-8, D.Lgs. 10/2026",
    "N6.2": "Art. 64, c. 5, D.Lgs. 10/2026",
    "N6.3": "Art. 64, c. 6, lett. a), D.Lgs. 10/2026",
    "N6.4": "Art. 64, c. 6, lett. b), D.Lgs. 10/2026",
    "N6.7": "Art. 64, c. 6, lett. c), D.Lgs. 10/2026",
    "N6.9": "Art. 64, c. 2, D.Lgs. 10/2026",
    "N7": "Art. 150, D.Lgs. 10/2026",
}

#: References shipped by ``l10n_it`` before 2027, updated to the reference
#: given for the exoneration codes without a single Testo Unico IVA article
#: (see above). The same wording is shipped for more than one code ("Fuori
#: dall'Unione Europea" is both N2.2 and N7), so the code is part of the key:
#: the N2.2 tax keeps its wording and is left to the user, as for the other
#: operations whose article depends on the operation.
LEGACY_REFERENCES = {
    ("N7", "Fuori dall'Unione Europea"): "Art. 150, D.Lgs. 10/2026",
}


class AccountTax(models.Model):
    _inherit = "account.tax"

    l10n_it_law_reference_until_2026 = fields.Char(
        string="Law Reference until 2026",
        size=100,
        help="Reference cited on the documents dated before the Testo Unico "
        "IVA applies (1 January 2027). The law reference of the tax is "
        "copied here, and replaced by the Testo Unico IVA one, when the "
        "module is installed and when the Italian chart of accounts is "
        "loaded, so the standard field is the one used from 2027.",
    )

    def _l10n_it_tu_iva_get_tu_iva_reference(self):
        """Testo Unico IVA reference replacing the current law reference.

        Returns ``None`` when the tax already cites the Testo Unico IVA, or
        when the article of its exoneration code depends on the operation:
        such a reference is left to the user.
        """
        self.ensure_one()
        current_reference = self.l10n_it_law_reference
        legacy_key = (self.l10n_it_exempt_reason, current_reference)
        if legacy_key in LEGACY_REFERENCES:
            return LEGACY_REFERENCES[legacy_key]
        if not current_reference or not REPEALED_DECREE_RE.search(current_reference):
            return None
        return TU_IVA_REFERENCES.get(self.l10n_it_exempt_reason)

    @api.model
    def _l10n_it_tu_iva_update_law_references(self, taxes=None):
        """Cite the Testo Unico IVA in the law reference of the taxes.

        The previous reference is kept in ``l10n_it_law_reference_until_2026``
        for the documents dated before 2027. Only a reference citing a decree
        replaced by the Testo Unico IVA is updated, so the method is idempotent
        and a reference already citing the Testo Unico IVA is kept. A reference
        narrowed to a sub-clause is replaced by the article of its exoneration
        code: the wording of the sub-clause stays in the field used before
        2027, and the user can refine the new reference on the tax.

        Archived taxes are updated too: they can be restored for a document
        dated from 2027.
        """
        if taxes is None:
            taxes = self.with_context(active_test=False).search(
                [("l10n_it_law_reference", "!=", False)]
            )
        for tax in taxes:
            reference = tax._l10n_it_tu_iva_get_tu_iva_reference()
            if not reference:
                continue
            tax.write(
                {
                    "l10n_it_law_reference_until_2026": tax.l10n_it_law_reference,
                    "l10n_it_law_reference": reference,
                }
            )
