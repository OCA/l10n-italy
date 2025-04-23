# Copyright 2022 Simone Rubino - TAKOBI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

ASSET_TYPES = (
    "asset_receivable",
    "asset_cash",
    "asset_current",
    "asset_non_current",
    "asset_prepayments",
    "asset_fixed",
)
LIABILITY_TYPES = (
    "liability_payable",
    "liability_credit_card",
    "liability_current",
    "liability_non_current",
)


class AccountTax(models.Model):
    _inherit = "account.tax"

    # TODO remove?
    parent_tax_ids = fields.Many2many(
        "account.tax",
        "account_tax_filiation_rel",
        "child_tax",
        "parent_tax",
        string="Parent Taxes",
    )

    deductible_balance = fields.Float(compute="_compute_deductible_balance")
    undeductible_balance = fields.Float(compute="_compute_undeductible_balance")
    debit_balance = fields.Float(compute="_compute_debit_balance")
    credit_balance = fields.Float(compute="_compute_credit_balance")

    @api.depends_context(
        "from_date",
        "to_date",
        "company_ids",
        "target_move",
    )
    def _compute_deductible_balance(self):
        for tax in self:
            tax.deductible_balance = tax.credit_balance

    @api.depends_context(
        "from_date",
        "to_date",
        "company_ids",
        "target_move",
    )
    def _compute_undeductible_balance(self):
        for tax in self:
            account_ids = tax._get_accounts_tax().ids
            tax.undeductible_balance = tax._compute_tax_balance_by_accounts(
                exclude_account_ids=account_ids
            )

    @api.depends_context(
        "from_date",
        "to_date",
        "company_ids",
        "target_move",
    )
    def _compute_debit_balance(self):
        for tax in self:
            accounts = tax._get_accounts_tax()
            accounts = accounts.filtered(lambda a: a.account_type in LIABILITY_TYPES)
            account_ids = accounts.ids
            tax.debit_balance = tax._compute_tax_balance_by_accounts(
                account_ids=account_ids
            )

    @api.depends_context(
        "from_date",
        "to_date",
        "company_ids",
        "target_move",
    )
    def _compute_credit_balance(self):
        for tax in self:
            accounts = tax._get_accounts_tax()
            accounts = accounts.filtered(lambda a: a.account_type in ASSET_TYPES)
            account_ids = accounts.ids
            tax.credit_balance = tax._compute_tax_balance_by_accounts(
                account_ids=account_ids
            )

    def _get_accounts_tax(self):
        return self.mapped("invoice_repartition_line_ids.account_id") | self.mapped(
            "refund_repartition_line_ids.account_id"
        )

    def _compute_tax_balance_by_accounts(
        self, account_ids=None, exclude_account_ids=None
    ):
        balance_regular = self.compute_balance(
            tax_or_base="tax",
            financial_type="regular",
            account_ids=account_ids,
            exclude_account_ids=exclude_account_ids,
        )
        balance_refund = self.compute_balance(
            tax_or_base="tax",
            financial_type="refund",
            account_ids=account_ids,
            exclude_account_ids=exclude_account_ids,
        )
        return balance_regular + balance_refund

    def compute_balance(
        self,
        tax_or_base="tax",
        financial_type=None,
        account_ids=None,
        exclude_account_ids=None,
    ):
        balance = super().compute_balance(
            tax_or_base=tax_or_base,
            financial_type=financial_type,
        )
        if account_ids is not None:
            domain = self.get_move_lines_domain(
                tax_or_base=tax_or_base,
                financial_type=financial_type,
                account_ids=account_ids,
            )
            balance = self.env["account.move.line"].read_group(domain, ["balance"], [])[
                0
            ]["balance"]
            balance = balance and -balance or 0
        elif exclude_account_ids is not None:
            domain = self.get_move_lines_domain(
                tax_or_base=tax_or_base,
                financial_type=financial_type,
                exclude_account_ids=exclude_account_ids,
            )
            balance = self.env["account.move.line"].read_group(domain, ["balance"], [])[
                0
            ]["balance"]
            balance = balance and -balance or 0
        return balance

    def get_move_lines_domain(
        self,
        tax_or_base="tax",
        financial_type=None,
        account_ids=None,
        exclude_account_ids=None,
    ):
        domain = super().get_move_lines_domain(
            tax_or_base=tax_or_base,
            financial_type=financial_type,
        )
        if account_ids is not None:
            domain.append(
                (
                    "account_id",
                    "in",
                    account_ids,
                )
            )
        elif exclude_account_ids is not None:
            domain.append(
                (
                    "account_id",
                    "not in",
                    exclude_account_ids,
                )
            )
        return domain

    def _get_tax_amount(self):
        self.ensure_one()
        res = 0.0
        if self.amount_type == "group":
            for child in self.children_tax_ids:
                res += child.amount
        else:
            res = self.amount
        return res

    def _get_tax_name(self):
        self.ensure_one()
        name = self.name
        if self.parent_tax_ids and len(self.parent_tax_ids) == 1:
            name = self.parent_tax_ids[0].name
        return name

    def _compute_totals_tax(self, data):
        """
        Args:
            data: date range, journals and registry_type
        Returns:
            A tuple: (tax_name, base, tax, deductible, undeductible)

        """
        self.ensure_one()
        context = {
            "from_date": data["from_date"],
            "to_date": data["to_date"],
        }
        registry_type = data.get("registry_type", "customer")
        context["vat_registry_journal_ids"] = []
        if data.get("journal_ids"):
            context["vat_registry_journal_ids"] += data["journal_ids"]
        if data.get("rc_journal_ids"):
            context["vat_registry_journal_ids"] += data["rc_journal_ids"]

        tax = self.env["account.tax"].with_context(**context).browse(self.id)
        tax_name = tax._get_tax_name()
        base_balance = tax.base_balance
        balance = tax.balance
        deductible_balance = tax.deductible_balance
        undeductible_balance = tax.undeductible_balance
        debit_balance = tax.debit_balance
        credit_balance = tax.credit_balance
        if registry_type == "supplier":
            base_balance = -base_balance
            balance = -balance
            deductible_balance = -deductible_balance
            undeductible_balance = -undeductible_balance
            debit_balance = -debit_balance
            credit_balance = -credit_balance
        if registry_type == "customer" and tax.type_tax_use == "purchase":
            # case of reverse charge in sales VAT registry
            base_balance = -base_balance
        return (
            tax_name,
            base_balance,
            balance,
            deductible_balance,
            undeductible_balance,
            debit_balance,
            credit_balance,
        )
