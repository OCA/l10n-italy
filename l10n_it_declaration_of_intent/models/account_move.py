# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# Copyright 2022 Michele Rusticucci <michele.rusticucci@agilebg.com>
# Copyright 2025 Marco Colombo <marco.colombo@phi.technology>
# Copyright 2025 Sergio Corato <sergiocorato@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from collections import defaultdict

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.misc import format_date


class AccountMove(models.Model):
    _inherit = "account.move"

    declaration_of_intent_ids = fields.Many2many(
        comodel_name="l10n_it_declaration_of_intent.declaration",
        # compute="_compute_declarations",
        store=True,
        string="Declarations of intent",
    )
    declaration_of_intent_amount_ids = fields.One2many(
        comodel_name="account.move.intent",
        compute="_compute_declaration_amounts",
        inverse_name="move_id",
        store=True,
        string="Declarations of intent amounts",
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
                    lambda d: d.date_start <= valid_date <= d.date_end
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
            declarations = (
                invoice.declaration_of_intent_amount_ids.declaration_of_intent_id
            )

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
            if invoice.move_type.startswith("out"):
                pass
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
                            "Vostra dichiarazione d'intento del %s, "
                            "protocollo telematico nr %s."
                            % (
                                format_date(self.env, declaration.date),
                                declaration.telematic_protocol,
                            )
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

    @api.depends(
        "partner_id",
        "partner_id.commercial_partner_id",
        "declaration_of_intent_ids",
        "line_ids.tax_line_id",
    )
    def _compute_declaration_amounts(self):

        invoices = self.filtered(
            lambda move: move.partner_id and move.move_type.endswith("_invoice")
        )
        refunds = self.filtered(
            lambda move: move.partner_id and move.move_type.endswith("_refund")
        )

        for record in invoices:
            tax_summary = record._get_tax_summary()
            available_declarations = record._get_available_declarations(
                check_dates=True
            )

            # values = [fields.Command.clear()]
            # values = [(5,0,0)]
            record.declaration_of_intent_amount_ids = [(5, 0, 0)]
            values = []
            amount_per_declaration = {d: 0.0 for d in available_declarations}
            for tax_id, todo_amount in tax_summary.items():
                for declaration in available_declarations.sorted("date_end"):
                    if tax_id not in declaration.taxes_ids:
                        continue

                    available = (
                        declaration.available_amount
                        - amount_per_declaration[declaration]
                    )
                    if todo_amount <= available:
                        amount_per_declaration[declaration] += todo_amount
                        todo_amount = 0
                        break
                    else:
                        amount_per_declaration[declaration] += available
                        # amount_per_declaration[declaration] = declaration.available_amount
                        todo_amount -= available
            for d, amount in amount_per_declaration.items():
                # values.append(fields.Command.create({
                values.append(
                    [
                        0,
                        0,
                        {
                            "declaration_of_intent_id": d.id,
                            "move_id": record.id,
                            "amount": amount,
                        },
                    ]
                )
            record.declaration_of_intent_amount_ids = values

        for record in refunds:
            tax_summary = record._get_tax_summary()
            available_declarations = record._get_available_declarations(
                check_dates=False
            )

            # values = [fields.Command.clear()]
            values = [(5, 0, 0)]
            amount_per_declaration = {d: 0.0 for d in available_declarations}
            for tax_id, todo_amount in tax_summary.items():
                todo_amount = -todo_amount
                for declaration in available_declarations.sorted("date_end"):
                    if tax_id not in declaration.taxes_ids:
                        continue

                    available = (
                        declaration.used_amount - amount_per_declaration[declaration]
                    )
                    if todo_amount <= available:
                        amount_per_declaration[declaration] += todo_amount
                        todo_amount = 0
                        break
                    else:
                        amount_per_declaration[declaration] += available
                        # amount_per_declaration[declaration] = declaration.available_amount
                        todo_amount -= available
            for d, amount in amount_per_declaration.items():
                # values.append(fields.Command.create({
                values = [
                    (
                        0,
                        0,
                        {
                            "declaration_of_intent_id": d.id,
                            "move_id": record.id,
                            "amount": -amount,
                        },
                    )
                ]
            record.declaration_of_intent_amount_ids = values

        (self - invoices - refunds).declaration_of_intent_amount_ids = False

    def get_declarations_used_amounts(self, declarations):
        """Get used amount by declarations for this invoice."""
        self.ensure_one()
        cmp = self.currency_id.compare_amounts
        declarations_available_amounts = {
            declaration.id: declaration.available_amount for declaration in declarations
        }
        declarations_used_amounts = {}

        sign = 1 if self.move_type in ["out_invoice", "in_invoice"] else -1

        for tax_line in self.line_ids.filtered("tax_ids"):
            amount = sign * tax_line.price_subtotal
            matching_declarations = declarations.filtered(
                lambda declaration, line_taxes=tax_line.tax_ids: any(
                    tax in declaration.taxes_ids for tax in line_taxes
                )
            )
            for declaration in matching_declarations:
                if declaration.id not in declarations_used_amounts:
                    declarations_used_amounts[declaration.id] = 0

                if declaration == matching_declarations[-1]:
                    # If this is the last available declaration,
                    # assign all the remaining amount.

                    if cmp(amount, -declaration.used_amount) == -1:
                        raise UserError(
                            _("Available plafond insufficent.\n" "Excess value: %s")
                            % (amount + declaration.used_amount)
                        )
                    else:
                        declaration_used_amount = amount
                else:
                    declaration_available_amount = declarations_available_amounts[
                        declaration.id
                    ]
                    if cmp(amount, declaration_available_amount) == -1:
                        # amount can be negative (refund), make sure we don't get negative
                        if cmp(amount, 0.0) == 1:
                            declaration_used_amount = amount
                        else:
                            # use what's available
                            declaration_used_amount = -declaration.used_amount
                    else:
                        declaration_used_amount = declaration_available_amount

                declarations_available_amounts[
                    declaration.id
                ] -= declaration_used_amount
                declarations_used_amounts[declaration.id] += declaration_used_amount
                amount -= declaration_used_amount
        return declarations_used_amounts

    def check_declarations_amounts(self, declarations):
        """
        Compare this invoice's tax amounts and `declarations` plafond.

        An exception is raised if the plafond of the declarations
        is not sufficient for this invoice's taxes.
        """
        self.ensure_one()
        is_refund = self.move_type.endswith("_refund")

        declarations_amounts = self.get_declaration_residual_amounts(declarations)

        declarations_residual = sum(
            [declarations_amounts[da] for da in declarations_amounts]
        )
        if (
            not is_refund
            and self.currency_id.compare_amounts(declarations_residual, 0) == -1
        ):
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
        available_plafond = 0.0
        if self.move_type in ["in_invoice", "in_refund"]:
            plafond = self.company_id.declaration_yearly_limit_ids.filtered(
                lambda r: r.year == str(fields.first(declarations).date_start.year)
            )
            available_plafond = plafond.limit_amount - plafond.actual_used_amount
        declarations_amounts = {}
        # If the tax amount is 0, then there is no line representing the tax
        # so there will be no line having tax_line_id.
        # Therefore we choose instead the lines that
        # should generate the tax line i.e. the lines that have `tax_ids`
        tax_lines = self.line_ids.filtered("tax_ids")
        cmp = self.currency_id.compare_amounts
        for tax_line in tax_lines:
            # Move lines having `tax_ids` represent the base amount for those taxes
            if self.move_type.endswith("_refund"):
                amount = -tax_line.price_subtotal
            else:
                amount = tax_line.price_subtotal

            for declaration in declarations:
                if declaration.id not in declarations_amounts:
                    if (
                        self.move_type in ["in_invoice", "in_refund"]
                        and cmp(declaration.available_amount, available_plafond) == 1
                    ):
                        declarations_amounts[declaration.id] = available_plafond
                    else:
                        declarations_amounts[
                            declaration.id
                        ] = declaration.available_amount
                if any(tax in declaration.taxes_ids for tax in tax_line.tax_ids):
                    declarations_amounts[declaration.id] -= amount
                    # amount can be negative for refunds and
                    # declarations_amounts[declaration.id] can exceed
                    # declaration.limit_amount, so we limit it
                    if (
                        cmp(
                            declarations_amounts[declaration.id],
                            declaration.limit_amount,
                        )
                        == 1
                    ):
                        amount = (
                            declarations_amounts[declaration.id]
                            - declaration.limit_amount
                        )
                        declarations_amounts[declaration.id] = declaration.limit_amount
                    else:
                        amount = 0.0
        for declaration in declarations:
            # exclude amount from lines with invoice_id equals to self
            for line in declaration.line_ids.filtered(lambda l: l.invoice_id == self):
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

    # ok
    def _get_available_declarations(self, check_dates=True):
        self.ensure_one()
        invoice_type_short = self.get_type_short()
        if not invoice_type_short:
            return []
        all_declarations = self.env[
            "l10n_it_declaration_of_intent.declaration"
        ].get_all_for_partner(
            invoice_type_short,
            self.partner_id.commercial_partner_id.id,
            ignore_state=not check_dates,
        )

        all_declarations = all_declarations.filtered(
            lambda d: d.taxes_ids & self.line_ids.tax_ids
        )
        if check_dates:
            all_declarations = all_declarations.filtered(
                lambda d: d.state == "valid"
                and d.date_start <= fields.Date.today() <= d.date_end
            )
        return all_declarations

    def _get_tax_summary(self):
        self.ensure_one()
        tax_summary = defaultdict(lambda: 0.0)
        for line in self.line_ids.filtered(lambda li: len(li.tax_ids) == 1):
            tax_summary[line.tax_ids[0]] += line.price_subtotal
        return tax_summary


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    force_declaration_of_intent_id = fields.Many2one(
        comodel_name="l10n_it_declaration_of_intent.declaration",
        string="Force Declaration of Intent",
    )

    def _compute_tax_id(self):
        is_sale_document = self.is_sale_document(include_receipts=True)
        is_purchase_document = self.is_purchase_document(include_receipts=True)
        for line in self:
            fpos = (
                line.move_id.fiscal_position_id
                or line.move_id.partner_id.property_account_position_id
            )
            # If company_id is set, always filter taxes by the company
            if is_sale_document:
                product_taxes = line.product_id.taxes_id
            elif is_purchase_document:
                product_taxes = line.product_id.supplier_taxes_id
            else:
                return
            taxes = product_taxes.filtered(
                lambda r: not line.company_id or r.company_id == line.company_id
            )
            line.invoice_line_tax_ids = (
                fpos.map_tax(taxes, line.product_id, line.move_id.partner_shipping_id)
                if fpos
                else taxes
            )


class AccountMoveIntent(models.Model):
    _name = "account.move.intent"
    _description = "Declaration of intent Amount"

    currency_id = fields.Many2one(related="move_id.currency_id")
    declaration_of_intent_id = fields.Many2one(
        comodel_name="l10n_it_declaration_of_intent.declaration",
    )
    move_id = fields.Many2one(
        comodel_name="account.move",
    )
    amount = fields.Monetary()
