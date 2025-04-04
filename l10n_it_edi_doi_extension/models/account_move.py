from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _compute_l10n_it_edi_doi_use(self):
        sale_types = self.env["account.move"].get_sale_types()
        puchase_types = self.env["account.move"].get_purchase_types()
        total_types = sale_types + puchase_types
        for move in self:
            move.l10n_it_edi_doi_use = move.l10n_it_edi_doi_id or (
                move.country_code == "IT" and move.move_type in total_types
            )

    def _compute_l10n_it_edi_doi_amount(self):
        for move in self:
            if move.l10n_it_edi_doi_id.type == "out":
                return super()._compute_l10n_it_edi_doi_amount()
            tax = move.company_id.l10n_it_edi_doi_bill_tax_id
            if not tax or not move.l10n_it_edi_doi_id:
                move.l10n_it_edi_doi_amount = 0
                continue
            declaration_lines = move.invoice_line_ids.filtered(
                # The declaration tax cannot be used with other taxes on a single line
                # (checked in `_post`)
                lambda line, tax=tax: line.tax_ids.ids == tax.ids
            )
            move.l10n_it_edi_doi_amount = sum(declaration_lines.mapped("price_total"))

    def _compute_l10n_it_edi_doi_id(self):
        for move in self:
            if not move.l10n_it_edi_doi_use or (
                move.state != "draft" and not move.l10n_it_edi_doi_id
            ):
                move.l10n_it_edi_doi_id = False
                continue

            partner = move.partner_id.commercial_partner_id
            validity_warnings = move.l10n_it_edi_doi_id._get_validity_warnings(
                move.company_id, partner, move.currency_id, move.l10n_it_edi_doi_date
            )
            if move.l10n_it_edi_doi_id and not validity_warnings:
                continue

            doi_type = (
                "out" if move.move_type in ("out_invoice", "out_refund") else "in"
            )

            declaration = self.env[
                "l10n_it_edi_doi.declaration_of_intent"
            ]._fetch_valid_declaration_of_intent(
                move.company_id,
                partner,
                move.currency_id,
                move.l10n_it_edi_doi_date,
                doi_type=doi_type,
            )
            move.l10n_it_edi_doi_id = declaration
