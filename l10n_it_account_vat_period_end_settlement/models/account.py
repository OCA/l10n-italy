# Copyright 2011-2012 Domsense s.r.l. (<http://www.domsense.com>).
# Copyright 2012-15 Agile Business Group sagl (<http://www.agilebg.com>)
# Copyright 2015 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# Copyright 2021 Gianmarco Conte - Dinamiche Aziendali Srl (<www.dinamicheaziendali.it>)
# Copyright 2022 Simone Rubino - TAKOBI
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import math

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_is_zero


class AccountVatPeriodEndStatement(models.Model):
    def _compute_authority_vat_amount(self):
        for statement in self:
            debit_vat_amount = 0.0
            credit_vat_amount = 0.0
            generic_vat_amount = 0.0
            for debit_line in statement.debit_vat_account_line_ids:
                debit_vat_amount += debit_line.amount
            for credit_line in statement.credit_vat_account_line_ids:
                credit_vat_amount += credit_line.amount
            for generic_line in statement.generic_vat_account_line_ids:
                generic_vat_amount += generic_line.amount
            authority_amount = (
                debit_vat_amount
                - credit_vat_amount
                - generic_vat_amount
                - statement.previous_credit_vat_amount
                + statement.previous_debit_vat_amount
                - statement.tax_credit_amount
                + statement.interests_debit_vat_amount
                - statement.advance_amount
            )
            statement.authority_vat_amount = authority_amount

    def _compute_deductible_vat_amount(self):
        for statement in self:
            credit_vat_amount = 0.0
            for credit_line in statement.credit_vat_account_line_ids:
                credit_vat_amount += credit_line.amount
            statement.deductible_vat_amount = credit_vat_amount

    @api.depends(
        "state", "move_id.line_ids.amount_residual", "move_id.line_ids.currency_id"
    )
    def _compute_residual(self):
        precision = self.env.company.currency_id.decimal_places
        for statement in self:
            if not statement.move_id.exists():
                statement.residual = 0.0
                statement.reconciled = False
                statement.state = "draft"
                continue

            residual = 0.0
            for line in statement.move_id.line_ids:
                authority_vat_account_id = statement.authority_vat_account_id.id
                if line.account_id.id == authority_vat_account_id:
                    residual += line.amount_residual
            statement.residual = abs(residual)
            if float_is_zero(statement.residual, precision_digits=precision):
                statement.reconciled = True
                statement.state = "paid"
            else:
                statement.reconciled = False
                statement.state = "confirmed"

    @api.depends("move_id.line_ids.amount_residual")
    def _compute_lines(self):
        for statement in self:
            payment_lines = []
            if statement.move_id.exists():
                for line in statement.move_id.line_ids:
                    payment_lines.extend(
                        [
                            _f
                            for _f in [
                                rp.credit_move_id.id for rp in line.matched_credit_ids
                            ]
                            if _f
                        ]
                    )
                    payment_lines.extend(
                        [
                            _f
                            for _f in [
                                rp.debit_move_id.id for rp in line.matched_debit_ids
                            ]
                            if _f
                        ]
                    )
            statement.payment_ids = self.env["account.move.line"].browse(
                list(set(payment_lines))
            )

    @api.model
    def _get_default_interest(self):
        company = self.env.company
        return company.of_account_end_vat_statement_interest

    @api.model
    def _get_default_interest_percent(self):
        company = self.env.company
        if not company.of_account_end_vat_statement_interest:
            return 0
        return company.of_account_end_vat_statement_interest_percent

    _name = "account.vat.period.end.statement"
    _description = "VAT period end statement"
    _rec_name = "date"
    _order = "date DESC, id DESC"

    debit_vat_account_line_ids = fields.One2many(
        "statement.debit.account.line",
        "statement_id",
        "Debit VAT",
        help="The accounts containing the debit VAT amount to write-off",
        readonly=True,
    )
    credit_vat_account_line_ids = fields.One2many(
        "statement.credit.account.line",
        "statement_id",
        "Credit VAT",
        help="The accounts containing the credit VAT amount to write-off",
        readonly=True,
    )
    previous_credit_vat_account_id = fields.Many2one(
        "account.account",
        "Previous Credits VAT",
        help="Credit VAT from previous periods",
    )
    previous_credit_vat_amount = fields.Float(
        "Previous Credits VAT Amount",
        digits="Account",
    )
    previous_year_credit = fields.Boolean("Previous year credits")
    previous_debit_vat_account_id = fields.Many2one(
        "account.account",
        "Previous Debits VAT",
        help="Debit VAT from previous periods",
    )
    previous_debit_vat_amount = fields.Float(
        "Previous Debits VAT Amount",
        digits="Account",
    )
    interests_debit_vat_account_id = fields.Many2one(
        "account.account",
        "Due interests",
        help="Due interests for three-monthly statments",
    )
    interests_debit_vat_amount = fields.Float(
        "Due interests Amount",
        digits="Account",
    )
    tax_credit_account_id = fields.Many2one(
        "account.account",
        "Tax credits",
    )
    tax_credit_amount = fields.Float(
        "Tax credits Amount",
        digits="Account",
    )
    advance_account_id = fields.Many2one(
        "account.account",
        "Down payment",
    )
    advance_amount = fields.Float(
        "Down payment Amount",
        digits="Account",
    )
    advance_computation_method = fields.Selection(
        [
            ("1", "Storico"),
            ("2", "Previsionale"),
            ("3", "Analitico - effettivo"),
            ("4", '"4" (soggetti particolari)'),
        ],
        string="Down payment computation method",
    )
    generic_vat_account_line_ids = fields.One2many(
        "statement.generic.account.line",
        "statement_id",
        "Other VAT Credits / Debits or Tax Compensations",
    )
    authority_partner_id = fields.Many2one(
        "res.partner",
        "Tax Authority Partner",
    )
    authority_vat_account_id = fields.Many2one(
        "account.account",
        "Tax Authority VAT Account",
    )
    authority_vat_amount = fields.Float(
        "Authority VAT Amount",
        compute="_compute_authority_vat_amount",
        digits="Account",
    )
    # TODO is this field needed?
    deductible_vat_amount = fields.Float(
        "Deductible VAT Amount",
        compute="_compute_deductible_vat_amount",
        digits="Account",
    )
    journal_id = fields.Many2one(
        "account.journal",
        "Journal",
        required=True,
    )
    date = fields.Date(
        required=True,
        default=fields.Date.context_today,
    )
    move_id = fields.Many2one("account.move", "VAT settlement move", readonly=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("paid", "Paid"),
        ],
        readonly=True,
        default="draft",
    )
    payment_term_id = fields.Many2one(
        "account.payment.term",
        "Payment Term",
    )
    reconciled = fields.Boolean(
        "Paid/Reconciled",
        compute="_compute_residual",
        help="It indicates that the statement has been paid and the "
        "journal entry of the statement has been reconciled with "
        "one or several journal entries of payment.",
        store=True,
        readonly=True,
    )
    residual = fields.Float(
        string="Amount Due",
        compute="_compute_residual",
        store=True,
        help="Remaining amount due.",
        digits="Account",
    )
    payment_ids = fields.Many2many(
        "account.move.line", string="Payments", compute="_compute_lines", store=True
    )
    date_range_ids = fields.One2many("date.range", "vat_statement_id", "Periods")
    interest = fields.Boolean("Compute Interest", default=_get_default_interest)
    interest_percent = fields.Float(
        "Interest - Percent", default=_get_default_interest_percent
    )
    fiscal_page_base = fields.Integer("Last printed page", required=True, default=0)
    fiscal_year = fields.Char("Fiscal year for report")
    company_id = fields.Many2one(
        "res.company",
        "Company",
        default=lambda self: self.env.company,
    )
    annual = fields.Boolean("Annual prospect")
    account_ids = fields.Many2many(
        "account.account",
        string="Accounts filter",
        domain=lambda self: self._get_domain_account(),
    )

    def _get_domain_account(self):
        domain = [("exclude_from_vat_settlements", "=", False)]
        tax_ids = self.env["account.tax"].search(domain)
        account_ids = tax_ids.mapped("repartition_line_ids.account_id")
        return [("id", "in", account_ids.ids)]

    def unlink(self):
        for statement in self:
            if statement.state == "confirmed" or statement.state == "paid":
                raise UserError(
                    self.env._("You cannot delete a confirmed or paid statement")
                )
        res = super().unlink()
        return res

    def set_fiscal_year(self):
        for statement in self:
            if statement.date_range_ids:
                date = min([x.date_start for x in statement.date_range_ids])
                statement.update({"fiscal_year": date.year})

    def statement_draft(self):
        for statement in self:
            if statement.move_id:
                statement.move_id.button_cancel()
                statement.move_id.with_context(force_delete=True).unlink()
            statement.state = "draft"

    def _prepare_account_move_line(
        self, name, account_id, move_id, statement, statement_date, partner_id=False
    ):
        self.ensure_one()
        debit_vat_data = {
            "name": name,
            "account_id": account_id,
            "move_id": move_id,
            "journal_id": statement.journal_id.id,
            "debit": 0.0,
            "credit": 0.0,
            "date": statement_date,
            "company_id": statement.company_id.id,
            "partner_id": partner_id,
        }
        return debit_vat_data

    def create_move(self):
        move_obj = self.env["account.move"]
        for statement in self:
            statement_date = fields.Date.to_string(statement.date)
            move_data = {
                "ref": self.env._("VAT Settlement") + " - " + statement_date,
                "date": statement_date,
                "journal_id": statement.journal_id.id,
            }
            move = move_obj.create(move_data)
            statement.write({"move_id": move.id})
            lines_to_create = []

            self._add_debit_vat_data(lines_to_create, move, statement, statement_date)

            self._add_credit_vat_data(lines_to_create, move, statement, statement_date)

            self._add_previous_credit_vat_data(
                lines_to_create, move, statement, statement_date
            )

            self._add_tax_credit_data(lines_to_create, move, statement, statement_date)

            self._add_advance_vat_data(lines_to_create, move, statement, statement_date)

            self._add_previous_debit_data(
                lines_to_create, move, statement, statement_date
            )

            self._add_interests_data(lines_to_create, move, statement, statement_date)

            self._add_generic_vat_data(lines_to_create, move, statement, statement_date)

            self._add_end_debit_vat_data(
                lines_to_create, move, statement, statement_date
            )

            move.line_ids = lines_to_create
            move.action_post()
            statement.state = "confirmed"

        return True

    def _split_vat_data_payment_term(
        self,
        payment_term,
        move,
        statement_date,
        end_debit_vat_data,
    ):
        self.ensure_one()
        company = self.env.company
        currency = company.currency_id
        tax_amount = tax_amount_currency = self.authority_vat_amount
        untaxed_amount = untaxed_amount_currency = 0
        sign = 1 if move.is_inbound(include_receipts=True) else -1
        due_list = payment_term._compute_terms(
            statement_date,
            currency,
            company,
            tax_amount,
            tax_amount_currency,
            sign,
            untaxed_amount,
            untaxed_amount_currency,
        )
        payment_term_lines = []
        for term in due_list.get("line_ids"):
            current_line = end_debit_vat_data.copy()
            current_line["credit"] = term["company_amount"]
            current_line["date_maturity"] = term["date"]
            payment_term_lines.append((0, 0, current_line))
        return payment_term_lines

    def _add_end_debit_vat_data(self, lines_to_create, move, statement, statement_date):
        end_debit_vat_data = self._prepare_account_move_line(
            name=self.env._("Tax Authority VAT"),
            account_id=statement.authority_vat_account_id.id,
            move_id=move.id,
            statement=statement,
            statement_date=statement_date,
            partner_id=statement.authority_partner_id.id,
        )
        if statement.authority_vat_amount > 0:
            end_debit_vat_data["credit"] = math.fabs(statement.authority_vat_amount)
            payment_term = statement.payment_term_id
            if payment_term:
                payment_term_lines = self._split_vat_data_payment_term(
                    payment_term,
                    move,
                    statement_date,
                    end_debit_vat_data,
                )
                lines_to_create.extend(payment_term_lines)
            else:
                lines_to_create.append((0, 0, end_debit_vat_data))
        elif statement.authority_vat_amount < 0:
            end_debit_vat_data["debit"] = math.fabs(statement.authority_vat_amount)
            lines_to_create.append((0, 0, end_debit_vat_data))

    def _add_generic_vat_data(self, lines_to_create, move, statement, statement_date):
        for generic_line in statement.generic_vat_account_line_ids:
            generic_vat_data = self._prepare_account_move_line(
                name=self.env._("Other VAT Credits / Debits"),
                account_id=generic_line.account_id.id,
                move_id=move.id,
                statement=statement,
                statement_date=statement_date,
            )
            if generic_line.amount < 0:
                generic_vat_data["debit"] = math.fabs(generic_line.amount)
            else:
                generic_vat_data["credit"] = math.fabs(generic_line.amount)
            lines_to_create.append((0, 0, generic_vat_data))

    def _add_interests_data(self, lines_to_create, move, statement, statement_date):
        if statement.interests_debit_vat_amount:
            interests_data = self._prepare_account_move_line(
                name=self.env._("Due interests"),
                account_id=statement.interests_debit_vat_account_id.id,
                move_id=move.id,
                statement=statement,
                statement_date=statement_date,
            )
            if statement.interests_debit_vat_amount > 0:
                interests_data["debit"] = math.fabs(
                    statement.interests_debit_vat_amount
                )
            else:
                interests_data["credit"] = math.fabs(
                    statement.interests_debit_vat_amount
                )
            lines_to_create.append((0, 0, interests_data))

    def _add_previous_debit_data(
        self, lines_to_create, move, statement, statement_date
    ):
        if statement.previous_debit_vat_amount:
            previous_debit_vat_data = self._prepare_account_move_line(
                name=self.env._("Previous Debits VAT"),
                account_id=statement.previous_debit_vat_account_id.id,
                move_id=move.id,
                statement=statement,
                statement_date=statement_date,
            )
            if statement.previous_debit_vat_amount > 0:
                previous_debit_vat_data["debit"] = math.fabs(
                    statement.previous_debit_vat_amount
                )
            else:
                previous_debit_vat_data["credit"] = math.fabs(
                    statement.previous_debit_vat_amount
                )
            lines_to_create.append((0, 0, previous_debit_vat_data))

    def _add_advance_vat_data(self, lines_to_create, move, statement, statement_date):
        if statement.advance_amount:
            advance_vat_data = self._prepare_account_move_line(
                name=self.env._("Tax Credits"),
                account_id=statement.advance_account_id.id,
                move_id=move.id,
                statement=statement,
                statement_date=statement_date,
            )
            if statement.advance_amount < 0:
                advance_vat_data["debit"] = math.fabs(statement.advance_amount)
            else:
                advance_vat_data["credit"] = math.fabs(statement.advance_amount)
            lines_to_create.append((0, 0, advance_vat_data))

    def _add_tax_credit_data(self, lines_to_create, move, statement, statement_date):
        if statement.tax_credit_amount:
            tax_credit_vat_data = self._prepare_account_move_line(
                name=self.env._("Tax Credits"),
                account_id=statement.tax_credit_account_id.id,
                move_id=move.id,
                statement=statement,
                statement_date=statement_date,
            )
            if statement.tax_credit_amount < 0:
                tax_credit_vat_data["debit"] = math.fabs(statement.tax_credit_amount)
            else:
                tax_credit_vat_data["credit"] = math.fabs(statement.tax_credit_amount)
            lines_to_create.append((0, 0, tax_credit_vat_data))

    def _add_previous_credit_vat_data(
        self, lines_to_create, move, statement, statement_date
    ):
        if statement.previous_credit_vat_amount:
            previous_credit_vat_data = self._prepare_account_move_line(
                name=self.env._("Previous Credits VAT"),
                account_id=statement.previous_credit_vat_account_id.id,
                move_id=move.id,
                statement=statement,
                statement_date=statement_date,
            )
            if statement.previous_credit_vat_amount < 0:
                previous_credit_vat_data["debit"] = math.fabs(
                    statement.previous_credit_vat_amount
                )
            else:
                previous_credit_vat_data["credit"] = math.fabs(
                    statement.previous_credit_vat_amount
                )
            lines_to_create.append((0, 0, previous_credit_vat_data))

    def _add_credit_vat_data(self, lines_to_create, move, statement, statement_date):
        for credit_line in statement.credit_vat_account_line_ids:
            if credit_line.amount != 0.0:
                credit_vat_data = self._prepare_account_move_line(
                    name=self.env._("Credit VAT"),
                    account_id=credit_line.account_id.id,
                    move_id=move.id,
                    statement=statement,
                    statement_date=statement_date,
                )
                if credit_line.amount < 0:
                    credit_vat_data["debit"] = math.fabs(credit_line.amount)
                else:
                    credit_vat_data["credit"] = math.fabs(credit_line.amount)
                lines_to_create.append((0, 0, credit_vat_data))

    def _add_debit_vat_data(self, lines_to_create, move, statement, statement_date):
        for debit_line in statement.debit_vat_account_line_ids:
            if debit_line.amount != 0.0:
                debit_vat_data = self._prepare_account_move_line(
                    name=self.env._("Debit VAT"),
                    account_id=debit_line.account_id.id,
                    move_id=move.id,
                    statement=statement,
                    statement_date=statement_date,
                )
                if debit_line.amount > 0:
                    debit_vat_data["debit"] = math.fabs(debit_line.amount)
                else:
                    debit_vat_data["credit"] = math.fabs(debit_line.amount)
                lines_to_create.append((0, 0, debit_vat_data))

    def _get_previous_statements(self):
        self.ensure_one()
        prev_statements = self.search(
            [
                ("date", "<", self.date),
                ("annual", "=", False),
            ],
            order="date desc",
        )
        prev_statements_same_accounts = prev_statements.filtered(
            lambda s: s.account_ids == self.account_ids
        )
        return prev_statements_same_accounts

    def compute_amounts(self):
        decimal_precision_obj = self.env["decimal.precision"]
        debit_line_model = self.env["statement.debit.account.line"]
        credit_line_model = self.env["statement.credit.account.line"]
        for statement in self:
            statement.previous_debit_vat_amount = 0.0
            prev_statements = statement._get_previous_statements()
            if prev_statements and not statement.annual:
                prev_statement = prev_statements[0]
                if (
                    prev_statement.residual > 0
                    and prev_statement.authority_vat_amount > 0
                ):
                    statement.write(
                        {"previous_debit_vat_amount": prev_statement.residual}
                    )
                elif prev_statement.authority_vat_amount < 0:
                    statement.write(
                        {
                            "previous_credit_vat_amount": (
                                -prev_statement.authority_vat_amount
                            )
                        }
                    )
                    company = statement.company_id or self.env.company
                    statement_fiscal_year_dates = company.compute_fiscalyear_dates(
                        statement.date_range_ids
                        and statement.date_range_ids[0].date_start
                        or statement.date
                    )
                    prev_statement_fiscal_year_dates = company.compute_fiscalyear_dates(
                        prev_statement.date_range_ids
                        and prev_statement.date_range_ids[0].date_start
                        or prev_statement.date
                    )
                    if (
                        prev_statement_fiscal_year_dates["date_to"]
                        < statement_fiscal_year_dates["date_from"]
                    ):
                        statement.write({"previous_year_credit": True})

            credit_line_ids, debit_line_ids = self._get_credit_debit_lines(statement)

            for debit_line in statement.debit_vat_account_line_ids:
                debit_line.unlink()
            for credit_line in statement.credit_vat_account_line_ids:
                credit_line.unlink()
            for debit_vals in debit_line_ids:
                debit_vals.update({"statement_id": statement.id})
                debit_line_model.create(debit_vals)
            for credit_vals in credit_line_ids:
                credit_vals.update({"statement_id": statement.id})
                credit_line_model.create(credit_vals)

            interest_amount = 0.0
            # if exits Delete line with interest
            acc_id = self.get_account_interest().id
            statement.interests_debit_vat_account_id = None
            statement.interests_debit_vat_amount = interest_amount

            # Compute interest
            if statement.interest and statement.authority_vat_amount > 0:
                interest_amount = round(
                    statement.authority_vat_amount
                    * (float(statement.interest_percent) / 100),
                    decimal_precision_obj.precision_get("Account"),
                )
            # Add line with interest
            if interest_amount:
                statement.interests_debit_vat_account_id = acc_id
                statement.interests_debit_vat_amount = interest_amount
        return True

    def _set_debit_lines(self, debit_tax, debit_line_ids, statement):
        total = 0.0
        for period in statement.date_range_ids:
            total += debit_tax._compute_totals_tax(
                {
                    "from_date": period.date_start,
                    "to_date": period.date_end,
                    "registry_type": "customer",
                }
            )[5]  # position 5 is debit balance
        debit_account_id = False
        if total:
            # For 0% taxes, account is not used
            debit_accounts = debit_tax._get_debit_accounts()
            if not debit_accounts:
                raise UserError(
                    self.env._(
                        "The tax %s has no debit account defined. "
                        "Please define it in the tax form."
                    )
                    % debit_tax.name
                )
            if len(debit_accounts) > 1:
                raise UserError(
                    self.env._(
                        "The tax %s has more than one debit account defined. "
                        "Please define only one in the tax form."
                    )
                    % debit_tax.name
                )
            debit_account_id = debit_accounts.id
        debit_line_ids.append(
            {
                "account_id": debit_account_id,
                "tax_id": debit_tax.id,
                "amount": total,
            }
        )

    def _set_credit_lines(self, credit_tax, credit_line_ids, statement):
        total = 0.0
        for period in statement.date_range_ids:
            total += credit_tax._compute_totals_tax(
                {
                    "from_date": period.date_start,
                    "to_date": period.date_end,
                    "registry_type": "supplier",
                }
            )[3]  # position 3 is deductible part
        credit_account_id = False
        if total:
            credit_accounts = credit_tax._get_credit_accounts()
            if not credit_accounts:
                raise UserError(
                    self.env._(
                        "The tax %s has no credit account defined. "
                        "Please define it in the tax form."
                    )
                    % credit_tax.name
                )
            if len(credit_accounts) > 1:
                raise UserError(
                    self.env._(
                        "The tax %s has more than one credit account defined. "
                        "Please define only one in the tax form."
                    )
                    % credit_tax.name
                )
            credit_account_id = credit_accounts.id
        credit_line_ids.append(
            {
                "account_id": credit_account_id,
                "tax_id": credit_tax.id,
                "amount": total,
            }
        )

    def _get_credit_debit_lines(self, statement):
        credit_line_ids = []
        debit_line_ids = []
        tax_model = self.env["account.tax"]
        taxes = tax_model.search(
            [
                ("exclude_from_vat_settlements", "=", False),
                ("type_tax_use", "in", ["sale", "purchase"]),
            ]
        )
        for tax in taxes:
            debit_accounts = tax._get_debit_accounts()
            credit_accounts = tax._get_credit_accounts()
            if debit_accounts:
                if (
                    all(debit_accounts.ids) in statement.account_ids.ids
                    or not statement.account_ids
                ):
                    self._set_debit_lines(tax, debit_line_ids, statement)
            if credit_accounts:
                if (
                    all(credit_accounts.ids) in statement.account_ids.ids
                    or not statement.account_ids
                ):
                    self._set_credit_lines(tax, credit_line_ids, statement)

        return credit_line_ids, debit_line_ids

    @api.onchange("authority_partner_id")
    def on_change_partner_id(self):
        self.authority_vat_account_id = (
            self.authority_partner_id.property_account_payable_id.id
        )

    @api.onchange("interest")
    def onchange_interest(self):
        company = self.env.company
        self.interest_percent = company.of_account_end_vat_statement_interest_percent

    def get_account_interest(self):
        company = self.env.company
        if company.of_account_end_vat_statement_interest or any(
            [s.interest for s in self]
        ):
            if not company.of_account_end_vat_statement_interest_account_id:
                raise UserError(
                    self.env._("The account for vat interest must be configurated")
                )

        return company.of_account_end_vat_statement_interest_account_id


class StatementDebitAccountLine(models.Model):
    _name = "statement.debit.account.line"
    _description = "VAT Settlement debit account line"

    account_id = fields.Many2one("account.account", "Account", required=False)
    tax_id = fields.Many2one("account.tax", "Tax", required=True)
    statement_id = fields.Many2one("account.vat.period.end.statement", "VAT Settlement")
    amount = fields.Float(required=True, digits="Account")


class StatementCreditAccountLine(models.Model):
    _name = "statement.credit.account.line"
    _description = "VAT Settlement credit account line"

    account_id = fields.Many2one("account.account", "Account", required=False)
    tax_id = fields.Many2one("account.tax", "Tax", required=True)
    statement_id = fields.Many2one("account.vat.period.end.statement", "VAT Settlement")
    amount = fields.Float(required=True, digits="Account")


class StatementGenericAccountLine(models.Model):
    _name = "statement.generic.account.line"
    _description = "VAT Settlement generic account line"

    account_id = fields.Many2one("account.account", "Account", required=True)
    statement_id = fields.Many2one("account.vat.period.end.statement", "VAT Settlement")
    amount = fields.Float(required=True, digits="Account")
    name = fields.Char("Description")


class AccountTax(models.Model):
    _inherit = "account.tax"
    exclude_from_vat_settlements = fields.Boolean(string="Exclude from VAT settlements")


class DateRange(models.Model):
    _inherit = "date.range"
    vat_statement_id = fields.Many2one(
        "account.vat.period.end.statement", "VAT Settlement"
    )
