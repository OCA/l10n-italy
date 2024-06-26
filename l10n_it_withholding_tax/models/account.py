# Copyright 2015 Alessandro Camilli (<http://www.openforce.it>)
# Copyright 2018 Lorenzo Battistini - Agile Business Group
# Copyright 2023 Simone Rubino - TAKOBI
# Copyright 2024 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.fields import first
from odoo.tools.float_utils import float_compare, float_round


class AccountFullReconcile(models.Model):
    _inherit = "account.full.reconcile"

    def _get_wt_moves(self):
        moves = self.mapped("reconciled_line_ids.move_id")
        wt_moves = self.env["withholding.tax.move"].search(
            [("wt_account_move_id", "in", moves.ids)]
        )
        return wt_moves

    @api.model
    def create(self, vals):
        res = super(AccountFullReconcile, self).create(vals)
        wt_moves = res._get_wt_moves()
        for wt_move in wt_moves:
            if wt_move.full_reconcile_id:
                wt_move.action_paid()
        return res

    def unlink(self):
        for rec in self:
            wt_moves = rec._get_wt_moves()
            super(AccountFullReconcile, rec).unlink()
            for wt_move in wt_moves:
                if not wt_move.full_reconcile_id:
                    wt_move.action_set_to_draft()
        return True


class AccountPartialReconcile(models.Model):
    _inherit = "account.partial.reconcile"

    def _wt_get_move_lines(self, vals):
        move_line_model = self.env["account.move.line"]
        debit_move_line = move_line_model.browse(vals.get("debit_move_id"))
        credit_move_line = move_line_model.browse(vals.get("credit_move_id"))
        return debit_move_line, credit_move_line

    def _wt_get_paying_invoice(self, move_lines):
        move_lines = move_lines.exists()
        invoices = move_lines.move_id.filtered(lambda move: move.is_invoice())
        # If we are reconciling a vendor bill and its refund,
        # we do not need to generate Withholding Tax Moves
        # or change the reconciliation amount
        in_refunding = invoices._wt_in_refunding()
        if not in_refunding:
            paying_invoice = first(invoices)
        else:
            paying_invoice = self.env["account.move"].browse()
        return paying_invoice

    @api.model
    def create(self, vals):
        # In case of WT The amount of reconcile mustn't exceed the tot net
        # amount. The amount residual will be full reconciled with amount net
        # and amount wt created with payment
        debit_move_line, credit_move_line = self._wt_get_move_lines(vals)
        move_lines = debit_move_line | credit_move_line
        paying_invoice = self._wt_get_paying_invoice(move_lines)
        reconcile_existing = False
        # Limit value of reconciliation
        if (
            paying_invoice
            and paying_invoice.withholding_tax
            and paying_invoice.amount_net_pay_residual
        ):
            # We must consider amount in foreign currency, if present
            # Note that this is always executed, for every reconciliation.
            # Thus, we must not change amount when not in withholding tax case
            amount = vals.get("amount_currency") or vals.get("amount")
            digits_rounding_precision = paying_invoice.company_id.currency_id.rounding
            if amount == 0.0:
                # it's a reconciliation with an existing move line
                if (
                    float_compare(
                        abs(debit_move_line.amount_residual),
                        abs(credit_move_line.amount_residual),
                        precision_rounding=digits_rounding_precision,
                    )
                    == 0
                ):
                    amount = abs(move_lines[0].amount_residual)
                    vals.update(
                        {
                            "amount": amount,
                            "credit_amount_currency": amount,
                            "debit_amount_currency": amount,
                        }
                    )
                    reconcile_existing = True
            if (
                float_compare(
                    amount,
                    paying_invoice.amount_net_pay_residual,
                    precision_rounding=digits_rounding_precision,
                )
                == 1
            ):
                vals.update(
                    {
                        "amount": paying_invoice.amount_net_pay_residual,
                        "credit_amount_currency": paying_invoice.amount_net_pay_residual,
                        "debit_amount_currency": paying_invoice.amount_net_pay_residual,
                    }
                )

        # Create reconciliation
        reconcile = super(AccountPartialReconcile, self).create(vals)
        # Avoid re-generate wt moves if the move line is an wt move.
        # It's possible if the user unreconciles a wt move under invoice

        moves = move_lines.move_id
        lines = self.env["account.move.line"].search(
            [
                ("withholding_tax_generated_by_move_id", "in", moves.ids),
                ("balance", "=", abs(vals.get("amount"))),
            ]
        )
        if not lines:
            for move in moves.filtered(lambda x: x.withholding_tax_amount):
                lines = self.env["account.move.line"].search(
                    [
                        ("withholding_tax_generated_by_move_id", "in", moves.ids),
                        ("balance", "=", abs(move.withholding_tax_amount)),
                        ("name", "=ilike", move.name),
                    ]
                )
                if lines:
                    reconcile_existing = True
        if lines:
            is_wt_move = True
            if not reconcile_existing:
                reconcile.generate_wt_moves(is_wt_move, lines)
        else:
            is_wt_move = False

        if paying_invoice:
            # Wt moves creation
            if (
                paying_invoice.withholding_tax_line_ids
                and not self.env.context.get("no_generate_wt_move")
                and not is_wt_move
                and (
                    debit_move_line.account_internal_type in ("receivable", "payable")
                    or credit_move_line.account_internal_type
                    in ("receivable", "payable")
                )
            ):
                # and not wt_existing_moves\
                if not reconcile_existing:
                    reconcile.generate_wt_moves(is_wt_move)

        return reconcile

    def _prepare_wt_move(self, vals):
        """
        Hook to change values before wt move creation
        """
        return vals

    @api.model
    def generate_wt_moves(self, is_wt_move, lines=None):
        wt_statement_obj = self.env["withholding.tax.statement"]
        # Reconcile lines
        line_payment_ids = []
        line_payment_ids.append(self.debit_move_id.id)
        line_payment_ids.append(self.credit_move_id.id)
        domain = [("id", "in", line_payment_ids)]
        rec_line_model = self.env["account.move.line"]
        rec_lines = rec_line_model.search(domain)

        # Search statements of competence
        wt_statements = wt_statement_obj.browse()
        rec_line_statement = rec_line_model.browse()
        for rec_line in rec_lines:
            domain = [("invoice_id", "=", rec_line.move_id.id)]
            wt_statements = wt_statement_obj.search(domain)
            if wt_statements:
                rec_line_statement = rec_line
                break
        # Search payment move
        rec_line_payment = rec_line_model.browse()
        for rec_line in rec_lines:
            if rec_line.id != rec_line_statement.id:
                rec_line_payment = rec_line
        # Generate wt moves
        wt_moves = []
        for wt_st in wt_statements:
            amount_wt = wt_st.get_wt_competence(self.amount)
            # Date maturity
            p_date_maturity = False
            payment_lines = wt_st.withholding_tax_id.payment_term.compute(
                amount_wt, rec_line_payment.date or False
            )
            if payment_lines and payment_lines[0]:
                p_date_maturity = payment_lines[0][0]
            wt_move_vals = {
                "statement_id": wt_st.id,
                "date": rec_line_payment.date,
                "partner_id": rec_line_statement.partner_id.id,
                "reconcile_partial_id": self.id,
                "payment_line_id": rec_line_payment.id,
                "credit_debit_line_id": rec_line_statement.id,
                "withholding_tax_id": wt_st.withholding_tax_id.id,
                "account_move_id": rec_line_payment.move_id.id or False,
                "date_maturity": p_date_maturity or rec_line_payment.date_maturity,
                "amount": amount_wt,
            }
            wt_move_vals = self._prepare_wt_move(wt_move_vals)
            wt_move = self.env["withholding.tax.move"].create(wt_move_vals)
            wt_moves.append(wt_move)
            # Generate account move
            if not is_wt_move:
                wt_move.generate_account_move()
            else:
                self.reconcile_exist_account_move(lines, rec_line_statement, amount_wt)
        return wt_moves

    @api.model
    def reconcile_exist_account_move(self, lines, rec_line_statement, amount_wt):
        line_to_reconcile = self.env["account.move.line"]
        for line in lines:
            if (
                line.account_id.user_type_id.type in ["payable", "receivable"]
                and line.partner_id
            ):
                line_to_reconcile = line
                break
        if line_to_reconcile:
            if line_to_reconcile.move_id.move_type in ["in_refund", "out_invoice"]:
                debit_move_id = rec_line_statement.id
                credit_move_id = line_to_reconcile.id
            else:
                debit_move_id = line_to_reconcile.id
                credit_move_id = rec_line_statement.id
            self.env["account.partial.reconcile"].with_context(
                no_generate_wt_move=True
            ).create(
                {
                    "debit_move_id": debit_move_id,
                    "credit_move_id": credit_move_id,
                    "amount": abs(amount_wt),
                    "credit_amount_currency": abs(amount_wt),
                    "debit_amount_currency": abs(amount_wt),
                }
            )

    def unlink(self):
        statements = []
        for rec in self:
            # To avoid delete if the wt move are paid
            domain = [("reconcile_partial_id", "=", rec.id), ("state", "!=", "due")]
            wt_moves = self.env["withholding.tax.move"].search(domain)
            if wt_moves:
                raise ValidationError(
                    _(
                        "Warning! Only Withholding Tax moves in Due status \
                    can be deleted"
                    )
                )
            # Statement to recompute
            domain = [("reconcile_partial_id", "=", rec.id)]
            wt_moves = self.env["withholding.tax.move"].search(domain)
            for wt_move in wt_moves:
                if wt_move.statement_id not in statements:
                    statements.append(wt_move.statement_id)

        res = super(AccountPartialReconcile, self).unlink()
        # Recompute statement values
        for st in statements:
            st._compute_total()
        return res


class AccountAbstractPayment(models.Model):
    _inherit = "account.payment"

    @api.model
    def default_get(self, fields):
        """
        Compute amount to pay proportionally to amount total - wt
        """
        rec = super(AccountAbstractPayment, self).default_get(fields)
        invoice_defaults = self.new(
            {"reconciled_invoice_ids": rec.get("reconciled_invoice_ids")}
        ).reconciled_invoice_ids

        if invoice_defaults and len(invoice_defaults) == 1:
            invoice = invoice_defaults[0]
            if (
                "withholding_tax_amount" in invoice
                and invoice["withholding_tax_amount"]
            ):
                coeff_net = invoice["amount_residual"] / invoice["amount_total"]
                rec["amount"] = invoice["amount_net_pay_residual"] * coeff_net
        return rec


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    withholding_tax_ids = fields.Many2many(
        "withholding.tax",
        "account_fiscal_position_withholding_tax_rel",
        "fiscal_position_id",
        "withholding_tax_id",
        string="Withholding Tax",
    )


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.depends(
        "invoice_line_ids.price_subtotal",
        "withholding_tax_line_ids.tax",
        "amount_total",
        # "payment_move_line_ids",
    )
    def _compute_amount_withholding_tax(self):
        dp_obj = self.env["decimal.precision"]
        for invoice in self:
            withholding_tax_amount = 0.0
            for wt_line in invoice.withholding_tax_line_ids:
                withholding_tax_amount += float_round(
                    wt_line.tax, dp_obj.precision_get("Account")
                )
            invoice.amount_net_pay = invoice.amount_total - withholding_tax_amount
            amount_net_pay_residual = invoice.amount_net_pay
            invoice.withholding_tax_amount = withholding_tax_amount

            reconciled_lines = invoice.line_ids.filtered(
                lambda line: line.account_id.user_type_id.type
                in ("receivable", "payable")
            )
            reconciled_amls = reconciled_lines.mapped(
                "matched_debit_ids.debit_move_id"
            ) + reconciled_lines.mapped("matched_credit_ids.credit_move_id")

            for line in reconciled_amls:
                if not line.withholding_tax_generated_by_move_id:
                    amount_net_pay_residual -= line.debit or line.credit
            if (
                float_compare(
                    amount_net_pay_residual, 0, dp_obj.precision_get("Account")
                )
                == -1
            ):
                amount_net_pay_residual = 0
            invoice.amount_net_pay_residual = float_round(
                amount_net_pay_residual, dp_obj.precision_get("Account")
            )

    withholding_tax = fields.Boolean("Withholding Tax")
    withholding_tax_in_print = fields.Boolean(
        "Show Withholding Tax In Print", default=True
    )
    withholding_tax_line_ids = fields.One2many(
        "account.invoice.withholding.tax",
        "invoice_id",
        "Withholding Tax Lines",
        copy=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    withholding_tax_amount = fields.Float(
        compute="_compute_amount_withholding_tax",
        digits="Account",
        string="Withholding tax Amount",
        store=True,
        readonly=True,
    )
    amount_net_pay = fields.Float(
        compute="_compute_amount_withholding_tax",
        digits="Account",
        string="Net To Pay",
        store=True,
        readonly=True,
    )
    amount_net_pay_residual = fields.Float(
        compute="_compute_amount_withholding_tax",
        digits="Account",
        string="Residual Net To Pay",
        store=True,
        readonly=True,
    )

    @api.onchange("invoice_line_ids")
    def _onchange_invoice_line_wt_ids(self):
        self.ensure_one()
        wt_taxes_grouped = self.get_wt_taxes_values()
        wt_tax_lines = [(5, 0, 0)]
        for tax in wt_taxes_grouped.values():
            wt_tax_lines.append((0, 0, tax))
        self.withholding_tax_line_ids = wt_tax_lines
        if len(wt_tax_lines) > 1:
            self.withholding_tax = True
        else:
            self.withholding_tax = False

    def action_post(self):
        """
        Split amount withholding tax on account move lines
        """
        dp_obj = self.env["decimal.precision"]
        res = super().action_post()

        for inv in self:
            # Rates
            rate_num = 0
            for move_line in inv.line_ids:
                if move_line.account_id.internal_type not in ["receivable", "payable"]:
                    continue
                rate_num += 1
            if rate_num:
                wt_rate = round(
                    inv.withholding_tax_amount / rate_num,
                    dp_obj.precision_get("Account"),
                )
            wt_residual = inv.withholding_tax_amount
            # Re-read move lines to assign the amounts of wt
            i = 0
            for move_line in inv.line_ids:
                if move_line.account_id.internal_type not in ["receivable", "payable"]:
                    continue
                i += 1
                if i == rate_num:
                    wt_amount = wt_residual
                else:
                    wt_amount = wt_rate
                wt_residual -= wt_amount
                # update line
                move_line.write({"withholding_tax_amount": wt_amount})
            # Create WT Statement
            if not self.env["withholding.tax.statement"].search(
                [("invoice_id", "=", inv.id)]
            ):
                inv.create_wt_statement()
        return res

    def get_wt_taxes_values(self):
        tax_grouped = {}
        for invoice in self:
            for line in invoice.invoice_line_ids:
                taxes = []
                for wt_tax in line.invoice_line_tax_wt_ids:
                    wt_tax = wt_tax._origin
                    res = wt_tax.compute_tax(line.price_subtotal)
                    tax = {
                        "id": wt_tax._origin.id,
                        "sequence": wt_tax.sequence,
                        "base": res["base"],
                        "tax": res["tax"],
                    }
                    taxes.append(tax)

                for tax in taxes:
                    val = {
                        "invoice_id": invoice.id,
                        "withholding_tax_id": tax["id"],
                        "tax": tax["tax"],
                        "base": tax["base"],
                        "sequence": tax["sequence"],
                    }

                    key = (
                        self.env["withholding.tax"]
                        .browse(tax["id"])
                        .get_grouping_key(val)
                    )

                    if key not in tax_grouped:
                        tax_grouped[key] = val
                    else:
                        tax_grouped[key]["tax"] += val["tax"]
                        tax_grouped[key]["base"] += val["base"]
        return tax_grouped

    def create_wt_statement(self):
        """
        Create one statement for each withholding tax
        """
        self.ensure_one()
        wt_statement_obj = self.env["withholding.tax.statement"]
        for inv_wt in self.withholding_tax_line_ids:
            wt_base_amount = inv_wt.base
            wt_tax_amount = inv_wt.tax
            if self.move_type in ["in_refund", "out_refund"]:
                wt_base_amount = -1 * wt_base_amount
                wt_tax_amount = -1 * wt_tax_amount
            val = {
                "wt_type": "",
                "date": self.date,
                "invoice_id": self.id,
                "partner_id": self.partner_id.id,
                "withholding_tax_id": inv_wt.withholding_tax_id.id,
                "base": wt_base_amount,
                "tax": wt_tax_amount,
            }
            wt_statement_obj.create(val)

    def _get_reconciled_info_JSON_values(self):
        payment_vals = super(AccountMove, self)._get_reconciled_info_JSON_values()
        for payment_val in payment_vals:
            move_line = self.env["account.move.line"].browse(payment_val["payment_id"])
            if move_line.withholding_tax_generated_by_move_id:
                payment_val["wt_move_line"] = True
            else:
                payment_val["wt_move_line"] = False
        return payment_vals

    def _wt_unlink_statements_move_states(self):
        """Move states that trigger the deletion of linked statements.

        When a posted move is changed in one of these states,
        its statements are deleted.
        """
        return "cancel", "draft"

    def _wt_unlink_statements(self):
        """Delete the statements linked to posted moves in `self`."""
        posted_moves = self.filtered_domain(
            [
                ("state", "=", "posted"),
            ],
        )
        if posted_moves:
            statements = self.env["withholding.tax.statement"].search(
                [
                    ("invoice_id", "in", posted_moves.ids),
                ],
            )
            statements.unlink()

    def write(self, vals):
        new_state = vals.get("state")
        if new_state in self._wt_unlink_statements_move_states():
            self._wt_unlink_statements()
        return super().write(vals)

    def _wt_in_refunding(self):
        return len(self) == 2 and set(self.mapped("move_type")) == {
            "in_invoice",
            "in_refund",
        }


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    withholding_tax_id = fields.Many2one("withholding.tax", string="Withholding Tax")
    withholding_tax_base = fields.Float(string="Withholding Tax Base")
    withholding_tax_amount = fields.Float(string="Withholding Tax Amount")
    withholding_tax_generated_by_move_id = fields.Many2one(
        "account.move", string="Withholding Tax generated from", readonly=True
    )

    def remove_move_reconcile(self):
        # When unreconcile a payment with a wt move linked, it will be
        # unreconciled also the wt account move
        for account_move_line in self:
            rec_move_ids = self.env["account.partial.reconcile"]
            domain = [
                (
                    "withholding_tax_generated_by_move_id",
                    "=",
                    account_move_line.move_id.id,
                )
            ]
            wt_mls = self.env["account.move.line"].search(domain)
            # Avoid wt move not in due state
            domain = [("wt_account_move_id", "in", wt_mls.mapped("move_id").ids)]
            wt_moves = self.env["withholding.tax.move"].search(domain)
            wt_moves.check_unlink()

            for wt_ml in wt_mls:
                rec_move_ids += wt_ml.matched_debit_ids
                rec_move_ids += wt_ml.matched_credit_ids
            rec_move_ids.unlink()
            # Delete wt move
            for wt_move in wt_mls.mapped("move_id"):
                wt_move.button_draft()
                wt_move.unlink()

        return super(AccountMoveLine, self).remove_move_reconcile()

    def _prepare_reconciliation_partials(self):
        wt_move_lines = self.filtered(lambda x: x.withholding_tax_amount != 0)
        if not wt_move_lines:
            return super()._prepare_reconciliation_partials()
        credit_lines = self.filtered(lambda line: line.credit)
        debit_line_ids = (self - credit_lines).ids
        partials_vals_list = []
        for credit_line in credit_lines:
            next_debit_line_id = debit_line_ids.pop(0) if debit_line_ids else False
            if next_debit_line_id:
                debit_line = self.browse(next_debit_line_id)
            total_amount_payment = debit_line.balance
            invoices = (credit_line | debit_line).move_id.filtered(
                lambda move: move.is_invoice()
            )
            in_refunding = invoices._wt_in_refunding()
            residual_amount = credit_line.move_id.amount_net_pay_residual
            if not in_refunding and total_amount_payment > residual_amount:
                total_amount_payment -= residual_amount
            else:
                residual_amount = total_amount_payment
            partials_vals_list.append(
                {
                    "amount": residual_amount,
                    "debit_amount_currency": residual_amount,
                    "credit_amount_currency": residual_amount,
                    "debit_move_id": debit_line.id,
                    "credit_move_id": credit_line.id,
                }
            )

        return partials_vals_list

    @api.model
    def _default_withholding_tax(self):
        result = []
        fiscal_position_id = self._context.get("fiscal_position_id", False)
        if fiscal_position_id:
            fp = self.env["account.fiscal.position"].browse(fiscal_position_id)
            wt_ids = fp.withholding_tax_ids.mapped("id")
            result.append((6, 0, wt_ids))
        return result

    invoice_line_tax_wt_ids = fields.Many2many(
        comodel_name="withholding.tax",
        relation="account_invoice_line_tax_wt",
        column1="invoice_line_id",
        column2="withholding_tax_id",
        string="W.T.",
        default=_default_withholding_tax,
    )


class AccountInvoiceWithholdingTax(models.Model):
    """
    Withholding tax lines in the invoice
    """

    _name = "account.invoice.withholding.tax"
    _description = "Invoice Withholding Tax Line"

    def _prepare_price_unit(self, line):
        price_unit = 0
        price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
        return price_unit

    @api.depends("base", "tax", "invoice_id.amount_untaxed")
    def _compute_coeff(self):
        for inv_wt in self:
            inv_wt.base_coeff = False
            inv_wt.tax_coeff = False
            if inv_wt.invoice_id.amount_untaxed:
                inv_wt.base_coeff = inv_wt.base / inv_wt.invoice_id.amount_untaxed
            if inv_wt.base:
                inv_wt.tax_coeff = inv_wt.tax / inv_wt.base

    invoice_id = fields.Many2one("account.move", string="Invoice", ondelete="cascade")
    withholding_tax_id = fields.Many2one(
        "withholding.tax", string="Withholding tax", ondelete="restrict"
    )
    sequence = fields.Integer("Sequence")
    base = fields.Float("Base")
    tax = fields.Float("Tax")
    base_coeff = fields.Float(
        "Base Coeff",
        compute="_compute_coeff",
        store=True,
        help="Coeff used\
         to compute amount competence in the riconciliation",
    )
    tax_coeff = fields.Float(
        "Tax Coeff",
        compute="_compute_coeff",
        store=True,
        help="Coeff used\
         to compute amount competence in the riconciliation",
    )
