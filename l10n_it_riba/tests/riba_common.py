#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.tests import common


class TestRibaCommon(common.TransactionCase):
    def setUp(self):
        super().setUp()
        tax_model = self.env["account.tax"]
        self.account_tax = (
            self.env.ref("l10n_it.2601", raise_if_not_found=False)
            or self.env.ref("l10n_generic_coa.tax_payable", raise_if_not_found=False)
            or self.env["account.account"].search(
                [("account_type", "=", "liability_current")], limit=1
            )
        )
        self.tax_22 = tax_model.create(
            {
                "name": "IVA 22 Sale",
                "description": "22",
                "amount": 22.00,
                "type_tax_use": "sale",
                "invoice_repartition_line_ids": [
                    (5, 0, 0),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "base",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "tax",
                            "account_id": self.account_tax.id,
                        },
                    ),
                ],
                "refund_repartition_line_ids": [
                    (5, 0, 0),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "base",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "tax",
                            "account_id": self.account_tax.id,
                        },
                    ),
                ],
            }
        )
        self.service_due_cost = self._create_service_due_cost()
        self.account_model = self.env["account.account"]
        self.move_line_model = self.env["account.move.line"]
        self.move_model = self.env["account.move"]
        self.slip_model = self.env["riba.slip"]
        self.partner = self.env.ref("base.res_partner_3")
        self.partner.vat = "IT01234567890"
        self.product1 = self.env.ref("product.product_product_5")
        self.sale_journal = self.env["account.journal"].search([("type", "=", "sale")])[
            0
        ]
        self.bank_journal = self.env["account.journal"].search(
            [("type", "=", "bank")], limit=1
        )
        self.payment_term1 = self._create_pterm()
        self.payment_term2 = self._create_pterm2()
        self.account_rec1_id = self.account_model.create(
            dict(
                code="custacc",
                name="customer account",
                account_type="asset_receivable",
                reconcile=True,
            )
        )
        self.sale_account = self.env["account.account"].search(
            [
                (
                    "account_type",
                    "=",
                    "income_other",
                )
            ],
            limit=1,
        )
        self.expenses_account = self.env["account.account"].search(
            [
                (
                    "account_type",
                    "=",
                    "expense",
                )
            ],
            limit=1,
        )
        self.bank_account = self.env["account.account"].search(
            [
                (
                    "account_type",
                    "=",
                    "asset_cash",
                )
            ],
            limit=1,
        )
        self.invoice = self._create_invoice()
        self.invoice2 = self._create_invoice()
        self.sbf_effects = self.env["account.account"].create(
            {
                "code": "STC",
                "name": "STC Bills (test)",
                "reconcile": True,
                "account_type": "asset_receivable",
            }
        )
        self.riba_account = self.env["account.account"].create(
            {
                "code": "RiBa",
                "name": "RiBa Account (test)",
                "account_type": "asset_fixed",
            }
        )
        self.past_due_account = self.env["account.account"].create(
            {
                "code": "PastDue",
                "name": "Past Due Bills Account (test)",
                "reconcile": True,
                "account_type": "asset_receivable",
            }
        )
        self.company_bank = self.env.ref("l10n_it_riba.company_bank")
        self.riba_config = self.create_config()
        self.account_payment_term_riba = self.env.ref(
            "l10n_it_riba.account_payment_term_riba"
        )
        self.company_bank.codice_sia = "AA555"

    def _create_service_due_cost(self):
        return self.env["product.product"].create(
            {
                "name": "Collection Fees",
                "type": "service",
                "taxes_id": [[6, 0, self.tax_22.ids]],
                "property_account_income_id": self._account_expense(),
            }
        )

    def _account_expense(self):
        return self.env["account.account"].create(
            {
                "code": "demoduecost",
                "name": "cashing fees",
                "account_type": "expense",
            }
        )

    def _create_invoice(self):
        # ----- Set invoice date to recent date in the system
        # ----- This solves problems with account_invoice_sequential_dates
        self.partner.property_account_receivable_id = self.account_rec1_id.id
        recent_date = (
            self.env["account.move"]
            .search([("invoice_date", "!=", False)], order="invoice_date desc", limit=1)
            .invoice_date
        )
        return self.env["account.move"].create(
            {
                "invoice_date": recent_date or fields.Date.today(),
                "move_type": "out_invoice",
                "journal_id": self.sale_journal.id,
                "partner_id": self.partner.id,
                "invoice_payment_term_id": self.payment_term1.id,
                "riba_partner_bank_id": self.partner.bank_ids[0].id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": self.product1.name,
                            "product_id": self.product1.id,
                            "quantity": 1.0,
                            "price_unit": 100.00,
                            "account_id": self.sale_account.id,
                            "tax_ids": [[6, 0, self.tax_22.ids]],
                        },
                    )
                ],
            }
        )

    def _create_pterm(self):
        return self.env["account.payment.term"].create(
            {
                "name": "RiBa 30/60",
                "riba": True,
                "riba_payment_cost": 5.00,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "value": "percent",
                            "months": 0,
                            "days": 30,
                            "value_amount": 0.50,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "value": "balance",
                            "months": 0,
                            "days": 60,
                        },
                    ),
                ],
            }
        )

    def _create_pterm2(self):
        return self.env["account.payment.term"].create(
            {
                "name": "RiBa 30",
                "riba": True,
                "riba_payment_cost": 5.00,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "value": "balance",
                            "months": 1,
                            "days": 1,
                        },
                    )
                ],
            }
        )

    def create_config(self):
        return self.env["riba.configuration"].create(
            {
                "name": "Subject To Collection",
                "type": "sbf",
                "bank_id": self.company_bank.id,
                "acceptance_journal_id": self.bank_journal.id,
                "credit_journal_id": self.bank_journal.id,
                "acceptance_account_id": self.sbf_effects.id,
                "credit_account_id": self.riba_account.id,
                "bank_account_id": self.bank_account.id,
                "bank_expense_account_id": self.expenses_account.id,
                "past_due_journal_id": self.bank_journal.id,
                "overdue_effects_account_id": self.past_due_account.id,
                "protest_charge_account_id": self.expenses_account.id,
            }
        )
