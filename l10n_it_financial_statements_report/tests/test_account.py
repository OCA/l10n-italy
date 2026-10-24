#  Copyright 2024 Simone Rubino - Aion Tech
#  Copyright 2026 Luca Orioli <lucaorioli@gmail.com>
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import tests


class TestAccount(tests.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.account_model = cls.env["account.account"]

    def test_type_prepayments(self):
        prepayment_account = self.account_model.search(
            [
                ("account_type", "=", "asset_prepayments"),
            ],
            limit=1,
        )
        self.assertEqual(
            prepayment_account.financial_statements_report_section, "assets"
        )

    def test_sign_prepayments(self):
        """Prepayments are assets: their balance keeps its sign."""
        account = self.account_model.create(
            {
                "code": "TEST.PREPAID",
                "name": "Test Prepayments",
                "account_type": "asset_prepayments",
            }
        )
        self.assertEqual(account.account_balance_sign, 1)

    def test_type_other_expenses(self):
        """Accounts of type "Other Expenses" are in the Expenses section."""
        account = self.account_model.create(
            {
                "code": "TEST.EXP.OTHER",
                "name": "Test Other Expenses",
                "account_type": "expense_other",
            }
        )
        self.assertEqual(account.financial_statements_report_section, "expenses")
