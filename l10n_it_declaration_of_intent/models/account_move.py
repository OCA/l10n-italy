# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# Copyright 2022 Michele Rusticucci <michele.rusticucci@agilebg.com>
# Copyright 2025 Marco Colombo <marco.colombo@phi.technology>
# Copyright 2025 Sergio Corato <sergiocorato@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from collections import defaultdict

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    declaration_of_intent_ids = fields.Many2many(
        comodel_name="l10n_it_declaration_of_intent.declaration",
        compute="_compute_declarations",
        # store=True,
        string="Declarations of intent",
    )

    declaration_of_intent_amount_ids = fields.One2many(
        string="Declarations of intent amounts",
        comodel_name="l10n_it_declaration_of_intent.declaration_line",
        inverse_name="invoice_id",
        compute="_compute_declaration_amounts",
        store=True,
    )

    def _compute_declarations(self):
        for record in self:
            record.declaration_of_intent_ids = (
                record.declaration_of_intent_amount_ids.declaration_id
            )

    # XXX verificare se serve
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

    # XXX verificare se serve
    @api.onchange("invoice_date")
    def _onchange_date_invoice(self):
        self._set_fiscal_position()

    # XXX verificare se serve
    @api.onchange("partner_id", "company_id")
    def _onchange_partner_id(self):
        res = super()._onchange_partner_id()
        self._set_fiscal_position()
        return res

    # XXX - da implementare / verificare
    def select_manually_declarations(self):
        self.ensure_one()
        action = self.env.ref(
            "l10n_it_declaration_of_intent.select_manually_declarations_action"
        ).read()[0]
        return action

    @api.depends(
        "partner_id",
        "partner_id.commercial_partner_id",
        "declaration_of_intent_ids",
        "line_ids",
        "line_ids.tax_line_id",
        "line_ids.price_subtotal",
    )
    def _compute_declaration_amounts(self):  # noqa: C901
        # at some point during creation partner_id and or line_ids may be empty
        invoices = self.filtered(
            lambda move: move.partner_id
            and move.line_ids
            and move.move_type.endswith("_invoice")
            and move.fiscal_position_id.valid_for_declaration_of_intent
        )
        refunds = self.filtered(
            lambda move: move.partner_id
            and move.line_ids
            and move.move_type.endswith("_refund")
            and move.fiscal_position_id.valid_for_declaration_of_intent
        )

        for record in invoices:
            cmp = record.currency_id.compare_amounts
            available_declarations = record._get_available_declarations(
                check_dates=True
            )
            tax_summary = record._get_tax_summary()
            # we're interest only in those taxes associated with
            # available_declarations
            tax_summary = {
                k: v
                for k, v in tax_summary.items()
                if k in available_declarations.taxes_ids
            }

            # 16.0 values = [fields.Command.clear()]
            values = [(5, 0, 0)]
            amount_per_declaration = {d: 0.0 for d in available_declarations}

            # handle forced declarations first
            # remove their amounts from tax_summary
            for line in record.line_ids.filtered(
                lambda li: li.force_declaration_of_intent_id
            ):
                declaration = line.force_declaration_of_intent_id
                available = (
                    declaration.available_amount - amount_per_declaration[declaration]
                )
                # try and assign the declaration
                if cmp(line.price_subtotal, available) <= 0:
                    amount_per_declaration[declaration] += line.price_subtotal
                    tax_summary[line.tax_ids[0]] -= line.price_subtotal
                    assert cmp(tax_summary[line.tax_ids[0]], 0.0) > 0
                else:
                    raise UserError(
                        _("Available plafond insufficent.\n" "Excess value: %s")
                        % (line.price_subtotal - available)
                    )

            for tax_id, todo_amount in tax_summary.items():
                for declaration in available_declarations.sorted("date_end"):
                    if tax_id not in declaration.taxes_ids:
                        continue
                    available = (
                        declaration.available_amount
                        - amount_per_declaration[declaration]
                    )

                    if cmp(todo_amount, available) == -1:
                        amount_per_declaration[declaration] += todo_amount
                        todo_amount = 0
                        break
                    else:
                        amount_per_declaration[declaration] += available
                        # amount_per_declaration[declaration] = declaration.available_amount
                        todo_amount -= available
                if cmp(todo_amount, 0.0) != 0:
                    raise UserError(
                        _("Available plafond insufficent.\n" "Excess value: %s")
                        % (todo_amount,)
                    )
            for d, amount in amount_per_declaration.items():
                if cmp(amount, 0.0) == 0:
                    continue
                # values.append(fields.Command.create({
                values.append(
                    (
                        0,
                        0,
                        {
                            "declaration_id": d.id,
                            "invoice_id": record.id,
                            "amount": amount,
                            "currency_id": record.currency_id.id,
                        },
                    )
                )
            record.declaration_of_intent_amount_ids = values

        # code for refunds is similar to the above, but:
        # - available declarations ignore dates and state
        # - amounts per declarations are negative (decrease used)
        # - (hence) available amount depends on used, not residual
        # - failure indicates a different event, a refund should never
        #   exceed the cumulative used amount no matter what, as it would
        #   exceed the amount on the invoice it refers to. The user is
        #   doing something very wrong: either the amount of the refund is
        #   wrong, or the original invoice didn't refer to declarations
        #   of intent, or something along the line.
        #   For invoices, exceeding the available amount requires the
        #   customer to create a new declaration, and which is (sort of)
        #   a regular workflow event.

        for record in refunds:
            cmp = record.currency_id.compare_amounts
            available_declarations = record._get_available_declarations(
                check_dates=False
            )
            tax_summary = record._get_tax_summary()
            # we're interest only in those taxes associated with
            # available_declarations
            tax_summary = {
                k: v
                for k, v in tax_summary.items()
                if k in available_declarations.taxes_ids
            }

            # 16.0 values = [fields.Command.clear()]
            values = [(5, 0, 0)]
            amount_per_declaration = {d: 0.0 for d in available_declarations}

            # handle forced declarations first
            # remove their amounts from tax_summary
            for line in record.line_ids.filtered(
                lambda li: li.force_declaration_of_intent_id
            ):
                declaration = line.force_declaration_of_intent_id
                available = (
                    declaration.available_amount - amount_per_declaration[declaration]
                )
                # try and assign the declaration
                assert line.price_subtotal >= 0  # TMP check if amounts are positive
                if cmp(line.price_subtotal, available) <= 0:
                    amount_per_declaration[declaration] -= line.price_subtotal
                    tax_summary[line.tax_ids[0]] -= line.price_subtotal
                    assert cmp(tax_summary[line.tax_ids[0]], 0.0) > 0
                else:
                    raise UserError(
                        _("Available plafond insufficent.\n" "Excess value: %s")
                        % (line.price_subtotal - available,)
                    )

            for tax_id, todo_amount in tax_summary.items():
                for declaration in available_declarations.sorted("date_end"):
                    if tax_id not in declaration.taxes_ids:
                        continue

                    available = (
                        declaration.used_amount - amount_per_declaration[declaration]
                    )
                    if cmp(todo_amount, available) <= 0:
                        amount_per_declaration[declaration] += todo_amount
                        todo_amount = 0
                        break
                    else:
                        amount_per_declaration[declaration] += available
                        # amount_per_declaration[declaration] = declaration.available_amount
                        todo_amount -= available
                if cmp(todo_amount, 0.0) != 0:
                    raise UserError(
                        _(
                            "Insufficient amount on declarations %r (tax %r).\n"
                            "Excess value: %s"
                        )
                        % (
                            available_declarations,
                            tax_id,
                            todo_amount,
                        )
                    )

            for d, amount in amount_per_declaration.items():
                if cmp(amount, 0.0) == 0:
                    continue
                # values.append(fields.Command.create({
                values.append(
                    (
                        0,
                        0,
                        {
                            "declaration_id": d.id,
                            "invoice_id": record.id,
                            "amount": -amount,
                            "currency_id": record.currency_id.id,
                        },
                    )
                )
            record.declaration_of_intent_amount_ids = values

        (self - invoices - refunds).declaration_of_intent_amount_ids = [(5, 0, 0)]

    def _get_available_declarations(self, check_dates=True):
        self.ensure_one()
        all_declarations = (
            self.reversed_entry_id.declaration_of_intent_amount_ids.declaration_id
        )
        invoice_type_short = self.get_type_short()
        if not invoice_type_short:
            return []
        all_declarations |= self.env[
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
                and d.date_start
                <= (self.invoice_date or fields.Date.today())
                <= d.date_end
            )
        return all_declarations

    def _get_tax_summary(self):
        self.ensure_one()
        tax_summary = defaultdict(lambda: 0.0)
        for line in self.line_ids.filtered(lambda li: len(li.tax_ids) == 1):
            tax_summary[line.tax_ids[0]] += line.price_subtotal
        return tax_summary

    def _post(self, soft=True):
        # XXX - potrebbe servire, per ora no
        # self._compute_declaration_amounts()

        posted = super()._post(soft)

        # XXX HACK - why this isn't triggered by its api.depends()?
        # line_ids.invoice_id.state has changed!
        posted.declaration_of_intent_ids._compute_amounts()
        return posted


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
