# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# Copyright 2022 Michele Rusticucci <michele.rusticucci@agilebg.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.misc import format_date


class AccountMove(models.Model):
    _inherit = "account.move"

    declaration_of_intent_ids = fields.Many2many(
        comodel_name="l10n_it_declaration_of_intent.declaration",
        string="Declarations of intent",
    )

    def _set_fiscal_position(self):
        for invoice in self:
            if invoice.partner_id:
                invoice_type_short = invoice.get_type_short()
                if not invoice_type_short:
                    continue
                all_declarations = self.env[
                    "l10n_it_declaration_of_intent.declaration"
                ].get_all_for_partner(
                    invoice_type_short,
                    invoice.partner_id.commercial_partner_id.id,
                )
                if not all_declarations:
                    return
                valid_date = invoice.invoice_date or fields.Date.context_today(invoice)

                valid_declarations = all_declarations.filtered(
                    lambda d, valid_d=valid_date: d.date_start <= valid_d <= d.date_end
                )
                if valid_declarations:
                    invoice.fiscal_position_id = valid_declarations[
                        0
                    ].fiscal_position_id.id
                elif invoice.fiscal_position_id and invoice.fiscal_position_id.id in [
                    d.fiscal_position_id.id for d in all_declarations
                ]:
                    invoice.fiscal_position_id = False

    def get_type_short(self):
        """
        Get in/out value from the invoice.

        This will then be matched with field
        l10n_it_declaration_of_intent.declaration.type.
        For instance:
        an invoice of type `in_refund` returns `in`,
        an invoice of type `out_refund` returns `out`,
        an invoice of type `entry` returns ``.
        """
        self.ensure_one()
        invoice_type_short = ""
        if self.move_type and "_" in self.move_type:
            invoice_type_short = self.move_type.split("_")[0]
        return invoice_type_short

    @api.onchange("invoice_date")
    def _onchange_date_invoice(self):
        self._set_fiscal_position()

    @api.onchange("partner_id", "company_id")
    def _onchange_partner_id(self):
        res = super()._onchange_partner_id()
        self._set_fiscal_position()
        return res

    def select_manually_declarations(self):
        self.ensure_one()
        action = self.env.ref(
            "l10n_it_declaration_of_intent.select_manually_declarations_action"
        ).read()[0]
        return action

    def _post(self, soft=True):
        posted = super()._post(soft)
        # Check if there is enough available amount on declarations
        for invoice in self.filtered(lambda m: m.is_invoice()):
            declarations = invoice.get_declarations()
            # If partner has no declarations, do nothing
            if not declarations:
                # If fiscal position is valid for declaration of intent,
                # there should be a valid declaration of intent
                if invoice.fiscal_position_id.valid_for_declaration_of_intent:
                    raise UserError(
                        _(
                            "Declaration of intent not found. Add new declaration or "
                            "change fiscal position and verify applied tax"
                        )
                    )
                else:
                    continue

            invoice.check_declarations_amounts(declarations)
            declarations_used_amounts = invoice.get_declarations_used_amounts(
                declarations
            )

            # Assign account move lines to declarations for each invoice
            # Get only lines with taxes
            lines = invoice.line_ids.filtered("tax_ids")
            if not lines:
                continue
            # Group lines by tax
            grouped_lines = self.get_move_lines_by_declaration(lines)
            invoice.update_declarations(declarations_used_amounts, grouped_lines)

        return posted

    def update_declarations(self, declarations_used_amounts, grouped_lines):
        """
        Update the declarations adding a new line representing this invoice.

        Also add a comment in this invoice stating which declaration is into.
        """
        self.ensure_one()
        is_sale_document = self.is_sale_document()
        for force_declaration in grouped_lines.keys():
            for tax, lines in grouped_lines[force_declaration].items():
                # Create a detail in declaration for every tax group
                amount = sum(line.balance for line in lines)
                if is_sale_document:
                    amount *= -1
                # Select right declaration(s)
                if force_declaration:
                    declaration_id_to_amount_dict = {force_declaration.id: amount}
                else:
                    declaration_id_to_amount_dict = declarations_used_amounts

                for declaration_id in declaration_id_to_amount_dict:
                    declaration = self.env[
                        "l10n_it_declaration_of_intent.declaration"
                    ].browse(declaration_id)
                    if tax not in declaration.taxes_ids:
                        continue
                    # avoid creating line with same invoice_id
                    declaration.line_ids.filtered(
                        lambda line: line.invoice_id == self
                    ).unlink()
                    declaration.line_ids = [
                        (
                            0,
                            0,
                            self._prepare_declaration_line(
                                declaration_id_to_amount_dict[declaration_id],
                                lines,
                                tax,
                            ),
                        ),
                    ]
                    # Link declaration to invoice
                    self.declaration_of_intent_ids = [(4, declaration.id)]
                    if is_sale_document:
                        cmt = self.narration or ""
                        msg = (
                            f"Vostra dichiarazione d'intento del "
                            f"{format_date(self.env, declaration.date)}, "
                            f"protocollo telematico nr "
                            f"{declaration.telematic_protocol}."
                        )
                        # Avoid duplication
                        if msg not in cmt:
                            if cmt.strip():
                                cmt += "\n\n" + msg
                            else:
                                cmt = msg
                        self.narration = cmt

    def _prepare_declaration_line(self, amount, lines, tax):
        """Dictionary used to create declaration line for this invoice."""
        self.ensure_one()
        return {
            "taxes_ids": [
                (6, 0, tax.ids),
            ],
            "move_line_ids": [
                (6, 0, lines.ids),
            ],
            "amount": amount,
            "invoice_id": self.id,
            "base_amount": self.amount_untaxed,
            "currency_id": self.currency_id.id,
        }

    @api.model
    def get_move_lines_by_declaration(self, lines):
        """Get account move lines grouped by the declaration forced in each line."""
        grouped_lines = {}
        invoice_line_model = self.env["account.move.line"]
        for line in lines:
            force_declaration = line.force_declaration_of_intent_id
            if force_declaration not in grouped_lines:
                grouped_lines.update({force_declaration: {}})

            tax = line.tax_ids[0]
            if tax not in grouped_lines[force_declaration]:
                grouped_lines[force_declaration].update(
                    {tax: invoice_line_model.browse()}
                )

            grouped_lines[force_declaration][tax] |= line
        return grouped_lines

    def get_declarations(self):
        """Get declarations linked directly or indirectly to this invoice."""
        self.ensure_one()
        declaration_model = self.env["l10n_it_declaration_of_intent.declaration"]
        if self.declaration_of_intent_ids:
            declarations = self.declaration_of_intent_ids
        else:
            declarations = declaration_model.with_context(
                ignore_state=True if self.move_type.endswith("_refund") else False
            ).get_valid(
                type_d=self.move_type.split("_")[0],
                partner_id=self.partner_id.id,
                date=self.invoice_date,
            )
        return declarations

    def get_declarations_used_amounts(self, declarations):
        """Get used amount by declarations for this invoice."""
        self.ensure_one()
        declarations_used_amounts = {}
        sign = 1 if self.move_type in ["out_invoice", "in_invoice"] else -1
        for tax_line in self.line_ids.filtered("tax_ids"):
            amount = sign * tax_line.price_subtotal
            for declaration in declarations:
                if declaration.id not in declarations_used_amounts:
                    declarations_used_amounts[declaration.id] = 0
                if any(tax in declaration.taxes_ids for tax in tax_line.tax_ids):
                    declarations_used_amounts[declaration.id] += amount
                    amount = 0.0
        return declarations_used_amounts

    def check_declarations_amounts(self, declarations):
        """
        Compare this invoice's tax amounts and `declarations` plafond.

        An exception is raised if the plafond of the declarations
        is not sufficient for this invoice's taxes.
        """
        self.ensure_one()
        declarations_amounts = self.get_declaration_residual_amounts(declarations)

        declarations_residual = sum(
            [declarations_amounts[da] for da in declarations_amounts]
        )
        if self.currency_id.compare_amounts(declarations_residual, 0) == -1:
            raise UserError(
                _("Available plafond insufficent.\n" "Excess value: %s")
                % (abs(declarations_residual))
            )

        # Check se con nota credito ho superato il plafond
        declaration_model = self.env["l10n_it_declaration_of_intent.declaration"]
        for declaration_id in declarations_amounts:
            declaration = declaration_model.browse(declaration_id)
            # declarations_amounts contains residual, so, if > limit_amount,
            # used_amount went < 0
            if (
                self.currency_id.compare_amounts(
                    declarations_amounts[declaration_id], declaration.limit_amount
                )
                == 1
            ):
                excess = abs(
                    declarations_amounts[declaration_id] - declaration.limit_amount
                )
                raise UserError(
                    _("Available plafond insufficent.\n" "Excess value: %s") % excess
                )
        return True

    def get_declaration_residual_amounts(self, declarations):
        """Get residual amount for every `declarations`."""
        declarations_amounts = {}
        # If the tax amount is 0, then there is no line representing the tax
        # so there will be no line having tax_line_id.
        # Therefore we choose instead the lines that
        # should generate the tax line i.e. the lines that have `tax_ids`
        tax_lines = self.line_ids.filtered("tax_ids")
        for tax_line in tax_lines:
            # Move lines having `tax_ids` represent the base amount for those taxes
            if self.move_type.endswith("_refund"):
                amount = -tax_line.price_subtotal
            else:
                amount = tax_line.price_subtotal

            for declaration in declarations:
                if declaration.id not in declarations_amounts:
                    declarations_amounts[declaration.id] = declaration.available_amount
                if any(tax in declaration.taxes_ids for tax in tax_line.tax_ids):
                    declarations_amounts[declaration.id] -= amount
        for declaration in declarations:
            # exclude amount from lines with invoice_id equals to self
            for line in declaration.line_ids.filtered(
                lambda dec_line: dec_line.invoice_id == self
            ):
                declarations_amounts[declaration.id] += line.amount
        return declarations_amounts

    def button_cancel(self):
        line_model = self.env["l10n_it_declaration_of_intent.declaration_line"]
        for invoice in self:
            # Force unlink of declaration details to compute used amount field
            lines = line_model.search([("invoice_id", "=", invoice.id)])
            if lines:
                for line in lines:
                    invoice.declaration_of_intent_ids = [(3, line.declaration_id.id)]
                lines.unlink()
        return super().button_cancel()


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    force_declaration_of_intent_id = fields.Many2one(
        comodel_name="l10n_it_declaration_of_intent.declaration",
        string="Force Declaration of Intent",
    )
