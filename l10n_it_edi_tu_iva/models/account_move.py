# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import re
from datetime import date

from markupsafe import escape

from odoo import api, fields, models

#: Decrees replaced by the Testo Unico IVA: a reference citing one of them is the
#: only one this module translates, so a reference already updated by the user
#: is kept.
REPEALED_DECREE_RE = re.compile(r"\b(?:633|331|41)/\d")

#: First date whose documents must cite the Testo Unico IVA
#: (D.Lgs. 19 January 2026, n. 10), in force from 1 January 2027.
TU_IVA_START_DATE = date(2027, 1, 1)

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
#: (art. 5, c. 3, art. 22, art. 139, art. 150, art. 157 ...), so the reference
#: configured on the tax is left untouched and the user sets the article of the
#: specific operation in ``l10n_it_tu_iva_law_reference`` on that tax.
#: ``N6.5``, ``N6.6`` and ``N6.8`` are missing too: since art. 64, c. 8, D.Lgs.
#: 10/2026 they no longer apply to operations carried out from 2027, so those
#: taxes have to be archived rather than given a new reference.
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

#: References shipped by ``l10n_it`` before 2027, replaced by the reference
#: given for the exoneration codes without a single Testo Unico IVA article
#: (see above). Matching on the text rather than on the exoneration code keeps
#: the references customized by the user untouched.
LEGACY_REFERENCES = {
    "Fuori dall'Unione Europea": "Art. 150, D.Lgs. 10/2026",
    "Art. 74-sexies DPR 633/1972": "Art. 150, D.Lgs. 10/2026",
}

#: Citations of the notes of the Italian fiscal positions, whose text is
#: printed on the invoice, and the Testo Unico IVA citation replacing them.
#: Only the citations shipped by ``l10n_it`` are matched: a note edited by the
#: user is printed as it is.
TU_IVA_NOTE_REFERENCES = {
    # Fiscal position "intra" (art. 17, c. 2, D.P.R. 633/1972 -> art. 64, c. 2)
    (
        "Article 17, Paragraph 2 of Presidential Decree No. 633 dated "
        "October 26, 1972"
    ): "Article 64, Paragraph 2, of Legislative Decree No. 10 dated "
    "January 19, 2026",
    "art. 17, comma 2 del DPR 26/10/1972 n. 633": (
        "art. 64, comma 2, del D.Lgs. 10/2026"
    ),
    # Fiscal position "split_payment_fiscal_position" (art. 17-ter -> art. 65)
    "art.17-ter of the D.P.R. 633/1972": "art. 65 of the D.Lgs. 10/2026",
    "art.17-ter del D.P.R. 633/1972": "art. 65 del D.Lgs. 10/2026",
    # Fiscal position "construction_fiscal_position" (art. 17, c. 6, lett. a)
    "art.17, comma 6, letter a, DPR 633/1972": "art. 64, comma 6, letter a, "
    "D.Lgs. 10/2026",
    "art. 17, comma 6, lettera a, DPR 633/1972": "art. 64, comma 6, lettera a, "
    "D.Lgs. 10/2026",
}


class AccountMove(models.Model):
    _inherit = "account.move"

    # Note of the fiscal position as printed on the invoice, citing the Testo
    # Unico IVA from 2027. `taxes_legal_notes` is not redeclared: the depends of
    # this module are merged with the ones of the parent override.
    l10n_it_tu_iva_note = fields.Html(
        compute="_compute_l10n_it_tu_iva_note",
        string="TU IVA note",
    )

    @api.depends(
        "fiscal_position_id.note",
        "invoice_date",
        "date",
        "reversed_entry_id.invoice_date",
        "company_id.account_fiscal_country_id",
    )
    def _compute_l10n_it_tu_iva_note(self):
        for move in self:
            note = move.fiscal_position_id.note
            if note and move._l10n_it_tu_iva_applies():
                for legacy, reference in TU_IVA_NOTE_REFERENCES.items():
                    note = note.replace(legacy, reference)
            move.l10n_it_tu_iva_note = note

    @api.depends(
        "line_ids.tax_ids",
        "line_ids.tax_ids.l10n_it_exempt_reason",
        "line_ids.tax_ids.l10n_it_law_reference",
        "line_ids.tax_ids.l10n_it_tu_iva_law_reference",
        "invoice_date",
        "date",
        "reversed_entry_id.invoice_date",
        "company_id.account_fiscal_country_id",
    )
    def _compute_taxes_legal_notes(self):
        res = super()._compute_taxes_legal_notes()
        for move in self:
            references = move._l10n_it_tu_iva_get_printed_references()
            if references:
                notes = "".join(f"<p>{escape(ref)}</p>" for ref in references)
                move.taxes_legal_notes = (move.taxes_legal_notes or "") + notes
        return res

    def _l10n_it_tu_iva_get_printed_references(self):
        """Normative references printed on the invoice, one per reference."""
        self.ensure_one()
        if not self.is_sale_document() or not self._l10n_it_tu_iva_applies():
            return []
        references = []
        for tax in self.line_ids.tax_ids.flatten_taxes_hierarchy():
            reference = self._l10n_it_tu_iva_get_reference(
                tax.l10n_it_exempt_reason,
                tax.l10n_it_law_reference,
                tax.l10n_it_tu_iva_law_reference,
            )
            if reference and reference not in references:
                references.append(reference)
        return references

    @api.model
    def _l10n_it_tu_iva_start_date(self):
        """First date of documents that have to cite the Testo Unico IVA.

        Kept as a method so that another module (or a specific company rule)
        can move the date without touching this one.
        """
        return TU_IVA_START_DATE

    def _l10n_it_tu_iva_reference_date(self):
        """Date of the document the invoice wording refers to.

        A credit note keeps the wording of the document it corrects: until
        2027 invoices dated 31/12/2026 can be issued and received, and a credit
        note issued in 2027 for a 2026 invoice must still cite the D.P.R.
        633/1972. The invoice date is used, not the date the document is sent
        to the SdI, and neither the accounting date.
        """
        self.ensure_one()
        move = self
        visited = self.browse()
        while move.reversed_entry_id and move.reversed_entry_id not in visited:
            visited |= move
            move = move.reversed_entry_id
        document_date = move.invoice_date or move.date or self.invoice_date or self.date
        return document_date or fields.Date.context_today(self)

    def _l10n_it_tu_iva_applies(self):
        """Whether the e-invoice of this document cites the Testo Unico IVA."""
        self.ensure_one()
        if self.company_id.account_fiscal_country_id.code != "IT":
            return False
        return (
            self._l10n_it_tu_iva_reference_date() >= self._l10n_it_tu_iva_start_date()
        )

    @api.model
    def _l10n_it_tu_iva_get_reference(
        self, exoneration_code, current_reference, tu_iva_reference=None
    ):
        """Testo Unico IVA reference replacing ``current_reference``, if any.

        The reference configured on the tax by the user (``tu_iva_reference``)
        always wins, so a tax created by the user cites the article the user
        chose. Otherwise only a reference citing a decree replaced by the Testo
        Unico IVA is translated: one already updated by the user is kept, which
        also makes the module idempotent.
        """
        if tu_iva_reference:
            return tu_iva_reference
        if current_reference in LEGACY_REFERENCES:
            return LEGACY_REFERENCES[current_reference]
        if not current_reference or not REPEALED_DECREE_RE.search(current_reference):
            return None
        return TU_IVA_REFERENCES.get(exoneration_code)

    @api.model
    def _l10n_it_edi_grouping_function_tax_lines(self, base_line, tax_data):
        # The grouping key carries the reference, so that taxes sharing a
        # Natura but citing different references produce distinct tax lines.
        # Called while rendering the e-invoice of a single move: the caller,
        # `_l10n_it_edi_get_values`, ensures it.
        res = super()._l10n_it_edi_grouping_function_tax_lines(base_line, tax_data)
        if not res or not self._l10n_it_tu_iva_applies():
            return res
        tax = tax_data["tax"]
        reference = self._l10n_it_tu_iva_get_reference(
            tax.l10n_it_exempt_reason,
            tax.l10n_it_law_reference,
            tax.l10n_it_tu_iva_law_reference,
        )
        if reference:
            res["l10n_it_law_reference"] = reference
        return res
