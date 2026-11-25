# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date

from markupsafe import escape

from odoo import api, fields, models

#: First date whose documents must cite the Testo Unico IVA
#: (D.Lgs. 19 January 2026, n. 10), in force from 1 January 2027.
TU_IVA_START_DATE = date(2027, 1, 1)

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
    # Fiscal position "split_payment_fiscal_position" (art. 17-ter -> art. 65).
    # The note says "ex art.": the replacement drops the "ex", since the Testo
    # Unico IVA is in force.
    "ex art.17-ter of the D.P.R. 633/1972": "art. 65 of the D.Lgs. 10/2026",
    "ex art.17-ter del D.P.R. 633/1972": "art. 65 del D.Lgs. 10/2026",
    # Fiscal position "construction_fiscal_position" (art. 17, c. 6, lett. a)
    "ex art.17, comma 6, letter a, DPR 633/1972": "art. 64, comma 6, letter a, "
    "D.Lgs. 10/2026",
    "ex art. 17, comma 6, lettera a, DPR 633/1972": "art. 64, comma 6, lettera "
    "a, D.Lgs. 10/2026",
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
    @api.depends_context("lang")
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
        "line_ids.tax_ids.l10n_it_law_reference_until_2026",
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
        if not self.is_sale_document():
            return []
        references = []
        applies = self._l10n_it_tu_iva_applies()
        for tax in self.line_ids.tax_ids.flatten_taxes_hierarchy():
            if applies:
                # The law reference already cites the Testo Unico IVA.
                reference = tax.l10n_it_law_reference
            else:
                reference = (
                    tax.l10n_it_law_reference_until_2026 or tax.l10n_it_law_reference
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
    def _l10n_it_edi_grouping_function_tax_lines(self, base_line, tax_data):
        # Before 2027 the law reference of the tax already cites the Testo
        # Unico IVA, so the reference of the document date is the one kept in
        # `l10n_it_law_reference_until_2026`. The reference is part of the
        # grouping key, so that taxes sharing a Natura but citing different
        # references produce distinct tax lines. The document is taken from
        # the base line, so the hook also works called on the model.
        res = super()._l10n_it_edi_grouping_function_tax_lines(base_line, tax_data)
        record = base_line.get("record")
        move = record.move_id if record else self
        if not res or move._l10n_it_tu_iva_applies():
            return res
        reference = tax_data["tax"].l10n_it_law_reference_until_2026
        if reference:
            res["l10n_it_law_reference"] = reference
        return res
