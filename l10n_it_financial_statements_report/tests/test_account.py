#  Copyright 2024 Simone Rubino - Aion Tech
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
