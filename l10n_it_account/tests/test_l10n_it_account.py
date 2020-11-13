from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestAccount(TransactionCase):
    def setUp(self):
        super(TestAccount, self).setUp()
        self.data_account_type_current_assets = self.env.ref(
            "account.data_account_type_current_assets"
        )
        self.data_account_type_current_liabilities = self.env.ref(
            "account.data_account_type_current_liabilities"
        )
        self.group_1 = self.env["account.group"].create(
            {
                "name": "1",
                "code_prefix_start": "it_account_",
            }
        )

    def test_group_constraint(self):
        self.env["account.account"].create(
            {
                "name": "it_account_1",
                "code": "it_account_1",
                "user_type_id": self.data_account_type_current_assets.id,
            }
        )
        with self.assertRaises(ValidationError):
            self.env["account.account"].create(
                {
                    "name": "it_account_2",
                    "code": "it_account_2",
                    "user_type_id": self.data_account_type_current_liabilities.id,
                }
            )
