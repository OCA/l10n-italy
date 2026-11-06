# Copyright 2025 Nextev Srl

from odoo import Command, _, api, fields, models
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

    @api.depends("l10n_it_edi_doi_total_amount")
    def _compute_l10n_it_edi_doi_warning(self):
        """Append a coverage warning when the bridge rows do not cover the
        invoice DOI amount. Core warnings (threshold, validity) are kept.
        """
        super()._compute_l10n_it_edi_doi_warning()
        for move in self.filtered("l10n_it_edi_doi_ids"):
            # Sale documents carry a signed amount (core), purchase ones do not
            doi_amount = abs(move.l10n_it_edi_doi_amount)
            if (
                move.currency_id.compare_amounts(
                    move.l10n_it_edi_doi_total_amount, doi_amount
                )
                >= 0
            ):
                continue
            covered = (
                f"{move.l10n_it_edi_doi_total_amount:.2f} {move.currency_id.symbol}"
            )
            total = f"{doi_amount:.2f} {move.currency_id.symbol}"
            coverage = _(
                "Warning: The total amount covered by declarations "
                "(%(covered)s) is less than the invoice DOI amount "
                "(%(total)s). Please adjust the amounts or add more "
                "declarations.",
                covered=covered,
                total=total,
            )
            move.l10n_it_edi_doi_warning = "\n\n".join(
                filter(None, [move.l10n_it_edi_doi_warning, coverage])
            )
        return  # W8110

    def _compute_l10n_it_edi_doi_amount(self):
        purchase_move_ids = self.filtered(lambda x: x.doi_type == "in")
        other_move_ids = self - purchase_move_ids
        super(AccountMove, other_move_ids)._compute_l10n_it_edi_doi_amount()
        for move in purchase_move_ids:
            tax = move._l10n_it_edi_doi_ext_get_declaration_tax()
            if not tax or not move.l10n_it_edi_doi_id:
                move.l10n_it_edi_doi_amount = 0
                continue
            declaration_lines = move._l10n_it_edi_doi_ext_get_declaration_lines(tax)
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

    def _l10n_it_edi_doi_ext_get_declaration_tax(self):
        """Get the DoI Tax to use with this line."""
        company = self.company_id
        return (
            company.l10n_it_edi_doi_bill_tax_id
            if self.is_purchase_document()
            else company.l10n_it_edi_doi_tax_id
        )

    def _l10n_it_edi_doi_ext_get_declaration_lines(self, doi_tax):
        """Extract the lines to be counted for DoI."""
        self.ensure_one()
        if self.l10n_it_edi_doi_id:
            lines = self.invoice_line_ids.filtered(
                lambda line, doi_tax=doi_tax: line._is_counted_for_doi(doi_tax)
            )
        else:
            lines = self.env["account.move.line"].browse()
        return lines

    def _l10n_it_edi_doi_ext_get_lines_messages(self, doi_tax):
        """Check that all the invoice lines are valid for the DoI."""
        self.ensure_one()
        errors = []
        for line in self.invoice_line_ids:
            if error := line._l10n_it_edi_doi_ext_get_validation_message(doi_tax):
                errors.append(error)
        return errors

    def _post(self, soft=True):
        errors = []
        for move in self:
            declaration = move.l10n_it_edi_doi_id
            doi_tax = move._l10n_it_edi_doi_ext_get_declaration_tax()
            if not doi_tax:
                continue
            declaration_lines = move._l10n_it_edi_doi_ext_get_declaration_lines(doi_tax)
            if declaration_lines and not declaration:
                errors.append(
                    _(
                        "Given the tax %s is applied, there should be a "
                        "Declaration of Intent selected.",
                        doi_tax.name,
                    )
                )
            if declaration:
                if not declaration_lines:
                    errors.append(
                        move.env._(
                            "Given the Declaration of Intent %(doi_name)s "
                            "is linked to this Move, at least one line "
                            "should contain the Tax %(doi_tax_name)s.",
                            doi_name=declaration.display_name,
                            doi_tax_name=doi_tax.name,
                        )
                    )
                if line_errors := move._l10n_it_edi_doi_ext_get_lines_messages(doi_tax):
                    errors.extend(line_errors)
        if errors:
            raise UserError("\n".join(errors))
        return super()._post(soft)

    def copy_data(self, default=None):
        """Carry the bridge lines onto credit notes only.

        A credit note must reverse the same declarations with the same amounts.
        A duplicate follows core instead: the split between declarations depends
        on their remaining amount at invoicing time, so it is not copied.
        Core _reverse_moves builds the credit note with copy(), so the lines are
        created while the move is still draft.
        The lines are copied whatever the current state of the declaration: a
        credit note reverses a consumption that already happened, so it must
        point to the same declaration even if it was terminated or revoked since.
        Core copy_data keeps l10n_it_edi_doi_id in that case as well (state and
        dates are not blocking when the amount is not positive).
        """
        data_list = super().copy_data(default)
        if not (default and default.get("reversed_entry_id")):
            return data_list
        for move, data in zip(self, data_list, strict=True):
            data["l10n_it_edi_doi_ids"] = [
                Command.create(
                    {
                        "declaration_id": link.declaration_id.id,
                        "amount": link.amount,
                        "sequence": link.sequence,
                    }
                )
                for link in move.l10n_it_edi_doi_ids
            ]
        return data_list

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
