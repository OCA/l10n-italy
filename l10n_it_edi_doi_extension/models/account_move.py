# Copyright 2025 Nextev Srl

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    doi_type = fields.Selection(
        [("in", "Issued from company"), ("out", "Received from customers")],
        compute="_compute_l10n_it_edi_doi_type",
    )

    # Multiple declarations of intent support
    l10n_it_edi_doi_ids = fields.One2many(
        "account.move.doi",
        "move_id",
        string="Declarations of Intent",
        help="Multiple declarations of intent linked to this invoice. "
        "Use this when the invoice amount exceeds a single declaration's threshold.",
    )
    l10n_it_edi_doi_count = fields.Integer(
        compute="_compute_l10n_it_edi_doi_count",
        string="DOI Count",
    )
    l10n_it_edi_doi_total_amount = fields.Monetary(
        compute="_compute_l10n_it_edi_doi_total_amount",
        string="Total DOI Amount",
        help="Total amount covered by all linked declarations of intent.",
    )

    @api.depends("l10n_it_edi_doi_ids")
    def _compute_l10n_it_edi_doi_count(self):
        for move in self:
            move.l10n_it_edi_doi_count = len(move.l10n_it_edi_doi_ids)

    @api.depends("l10n_it_edi_doi_ids.amount")
    def _compute_l10n_it_edi_doi_total_amount(self):
        for move in self:
            move.l10n_it_edi_doi_total_amount = sum(
                move.l10n_it_edi_doi_ids.mapped("amount")
            )

    @api.onchange("l10n_it_edi_doi_ids")
    def _onchange_l10n_it_edi_doi_ids(self):
        """Sync the first declaration with the standard field."""
        if self.l10n_it_edi_doi_ids:
            self.l10n_it_edi_doi_id = self.l10n_it_edi_doi_ids[0].declaration_id
        else:
            self.l10n_it_edi_doi_id = False

    @api.depends("move_type")
    def _compute_l10n_it_edi_doi_type(self):
        purchase_types = self.env["account.move"].get_purchase_types()
        sale_types = self.env["account.move"].get_sale_types()
        for move in self:
            if move.move_type in purchase_types:
                move.doi_type = "in"
            elif move.move_type in sale_types:
                move.doi_type = "out"
            else:
                move.doi_type = False

    def _compute_l10n_it_edi_doi_use(self):
        purchase_move_ids = self.filtered(lambda x: x.doi_type == "in")
        other_move_ids = self - purchase_move_ids
        super(AccountMove, other_move_ids)._compute_l10n_it_edi_doi_use()
        for move in purchase_move_ids:
            move.l10n_it_edi_doi_use = (
                move.l10n_it_edi_doi_id or move.country_code == "IT"
            )
        return  # W8110

    def _compute_l10n_it_edi_doi_warning(self):
        """Override to show custom warning when DOI amounts don't cover
        invoice total.
        """
        super()._compute_l10n_it_edi_doi_warning()
        for move in self:
            # Clear the warning first
            move.l10n_it_edi_doi_warning = ""

            # Only show warning if amounts don't match
            if (
                move.l10n_it_edi_doi_use
                and move.l10n_it_edi_doi_amount > 0
                and move.l10n_it_edi_doi_total_amount < move.l10n_it_edi_doi_amount
            ):
                covered = (
                    f"{move.l10n_it_edi_doi_total_amount:.2f} "
                    f"{move.currency_id.symbol}"
                )
                total = (
                    f"{move.l10n_it_edi_doi_amount:.2f} " f"{move.currency_id.symbol}"
                )
                move.l10n_it_edi_doi_warning = _(
                    "Warning: The total amount covered by declarations "
                    "(%(covered)s) is less than the invoice DOI amount "
                    "(%(total)s). Please adjust the amounts or add more "
                    "declarations.",
                    covered=covered,
                    total=total,
                )
        return  # W8110

    def _compute_l10n_it_edi_doi_amount(self):
        purchase_move_ids = self.filtered(lambda x: x.doi_type == "in")
        other_move_ids = self - purchase_move_ids
        super(AccountMove, other_move_ids)._compute_l10n_it_edi_doi_amount()
        for move in purchase_move_ids:
            tax = move.company_id.l10n_it_edi_doi_bill_tax_id
            if not tax or not move.l10n_it_edi_doi_id:
                move.l10n_it_edi_doi_amount = 0
                continue
            declaration_lines = move.invoice_line_ids.filtered(
                lambda line, tax=tax: tax in line.tax_ids
            )
            move.l10n_it_edi_doi_amount = sum(declaration_lines.mapped("price_total"))
        return  # W8110

    def _compute_l10n_it_edi_doi_id(self):
        purchase_move_ids = self.filtered(lambda x: x.doi_type == "in")
        other_move_ids = self - purchase_move_ids
        super(AccountMove, other_move_ids)._compute_l10n_it_edi_doi_id()
        for move in purchase_move_ids:
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

            declaration = self.env[
                "l10n_it_edi_doi.declaration_of_intent"
            ]._fetch_valid_declaration_of_intent(
                move.company_id,
                partner,
                move.currency_id,
                move.l10n_it_edi_doi_date,
                doi_type="in",
            )
            move.l10n_it_edi_doi_id = declaration
        return  # W8110

    def _post(self, soft=True):
        errors = []
        for move in self:
            declaration = move.l10n_it_edi_doi_id
            doi_bill_tax = move.company_id.l10n_it_edi_doi_bill_tax_id
            if not doi_bill_tax:
                continue
            declaration_lines = move.invoice_line_ids.filtered(
                lambda line, doi_bill_tax=doi_bill_tax: doi_bill_tax in line.tax_ids
            )
            if declaration_lines and not declaration:
                errors.append(
                    _(
                        "Given the tax %s is applied, there should be a "
                        "Declaration of Intent selected.",
                        doi_bill_tax.name,
                    )
                )
        if errors:
            raise UserError("\n".join(errors))
        return super()._post(soft)

    def _reverse_moves(self, default_values_list=None, cancel=False):
        """Override to copy DOI data from original invoice to refund."""
        reverse_moves = super()._reverse_moves(
            default_values_list=default_values_list, cancel=cancel
        )

        # Copy DOI links from original invoices to their refunds
        for reverse_move in reverse_moves:
            if not reverse_move.reversed_entry_id:
                continue

            original_move = reverse_move.reversed_entry_id
            # Copy DOI bridge records
            for doi_link in original_move.l10n_it_edi_doi_ids:
                self.env["account.move.doi"].create(
                    {
                        "move_id": reverse_move.id,
                        "declaration_id": doi_link.declaration_id.id,
                        "amount": doi_link.amount,
                        "sequence": doi_link.sequence,
                    }
                )

        return reverse_moves

    def action_open_declaration_of_intent(self):
        """Open declaration(s) of intent.

        If there are multiple declarations, open a list view.
        If there's only one, open its form view.
        """
        self.ensure_one()
        declaration_ids = self.l10n_it_edi_doi_ids.mapped("declaration_id").ids
        if not declaration_ids:
            declaration_ids = (
                [self.l10n_it_edi_doi_id.id] if self.l10n_it_edi_doi_id else []
            )

        if len(declaration_ids) > 1:
            return {
                "name": _("Declarations of Intent for %s", self.display_name),
                "type": "ir.actions.act_window",
                "view_mode": "list,form",
                "res_model": "l10n_it_edi_doi.declaration_of_intent",
                "domain": [("id", "in", declaration_ids)],
            }
        elif declaration_ids:
            return {
                "name": _("Declaration of Intent for %s", self.display_name),
                "type": "ir.actions.act_window",
                "view_mode": "form",
                "res_model": "l10n_it_edi_doi.declaration_of_intent",
                "res_id": declaration_ids[0],
            }
        else:
            raise UserError(
                _("No Declaration of Intent found for %s.", self.display_name)
            )
