# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestAccount(TransactionCase):
    def setUp(self):
        super(TestAccount, self).setUp()
        self.fiscal_position = (
            self.env["account.fiscal.position"]
            .sudo()
            .create(
                {
                    "name": "Test Fiscal Position",
                    "valid_for_declaration_of_intent": False,
                }
            )
        )

    def test_valid_for_declaration_of_intent(self):
        with self.assertRaises(ValidationError):
            self.fiscal_position.valid_for_declaration_of_intent = True
