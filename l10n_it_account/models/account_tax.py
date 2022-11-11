# Copyright 2022 Simone Rubino - TAKOBI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    cee_type = fields.Selection(
        [("sale", "Sale"), ("purchase", "Purchase")],
        string="Include in VAT register",
        help="Use in the case of tax with 'VAT integration'. This "
        "specifies the VAT register (sales / purchases) where the "
        "tax must be computed.",
    )
    parent_tax_ids = fields.Many2many(
        "account.tax",
        "account_tax_filiation_rel",
        "child_tax",
        "parent_tax",
        string="Parent Taxes",
    )

    deductible_balance = fields.Float(compute="_compute_deductible_balance")
    undeductible_balance = fields.Float(compute="_compute_undeductible_balance")

    @api.depends_context(
        "from_date",
        "to_date",
        "company_ids",
        "target_move",
    )
    def _compute_deductible_balance(self):
        for tax in self:
            account_ids = (
                tax.mapped("invoice_repartition_line_ids.account_id")
                | tax.mapped("refund_repartition_line_ids.account_id")
            ).ids
            balance_regular = tax.compute_balance(
                tax_or_base="tax", financial_type="regular", account_ids=account_ids
            )
            balance_refund = tax.compute_balance(
                tax_or_base="tax", financial_type="refund", account_ids=account_ids
            )
            tax.deductible_balance = balance_regular + balance_refund

    @api.depends_context(
        "from_date",
        "to_date",
        "company_ids",
        "target_move",
    )
    def _compute_undeductible_balance(self):
        for tax in self:
            account_ids = (
                tax.mapped("invoice_repartition_line_ids.account_id")
                | tax.mapped("refund_repartition_line_ids.account_id")
            ).ids
            balance_regular = tax.compute_balance(
                tax_or_base="tax",
                financial_type="regular",
                exclude_account_ids=account_ids,
            )
            balance_refund = tax.compute_balance(
                tax_or_base="tax",
                financial_type="refund",
                exclude_account_ids=account_ids,
            )
            tax.undeductible_balance = balance_regular + balance_refund

    def compute_balance(
        self,
        tax_or_base="tax",
        financial_type=None,
        account_ids=None,
        exclude_account_ids=None,
    ):
        balance = super(AccountTax, self).compute_balance(
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
        domain = super(AccountTax, self).get_move_lines_domain(
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
        if data.get("journal_ids"):
            context["vat_registry_journal_ids"] = data["journal_ids"]

        tax = self.env["account.tax"].with_context(**context).browse(self.id)
        tax_name = tax._get_tax_name()
        if not tax.children_tax_ids:
            base_balance = tax.base_balance
            balance = tax.balance
            deductible_balance = tax.deductible_balance
            undeductible_balance = tax.undeductible_balance
            if registry_type == "supplier":
                base_balance = -base_balance
                balance = -balance
                deductible_balance = -deductible_balance
                undeductible_balance = -undeductible_balance
            return (
                tax_name,
                base_balance,
                balance,
                deductible_balance,
                undeductible_balance,
            )
        else:
            # TODO remove?
            base_balance = tax.base_balance

            tax_balance = 0
            deductible = 0
            undeductible = 0
            for child in tax.children_tax_ids:
                child_balance = child.balance
                if (
                    data["registry_type"] == "customer" and child.cee_type == "sale"
                ) or (
                    data["registry_type"] == "supplier" and child.cee_type == "purchase"
                ):
                    # Prendo la parte di competenza di ogni registro e lo
                    # sommo sempre
                    child_balance = child_balance

                elif child.cee_type:
                    continue

                tax_balance += child_balance
                account_ids = (
                    child.mapped("invoice_repartition_line_ids.account_id")
                    | child.mapped("refund_repartition_line_ids.account_id")
                ).ids
                if account_ids:
                    deductible += child_balance
                else:
                    undeductible += child_balance
            if registry_type == "supplier":
                base_balance = -base_balance
                tax_balance = -tax_balance
                deductible = -deductible
                undeductible = -undeductible
            return (tax_name, base_balance, tax_balance, deductible, undeductible)
