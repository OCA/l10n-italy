#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.tests import Form

from .riba_common import TestRibaCommon


class TestAccountMove(TestRibaCommon):
    def test_select_commercial_partner_bank(self):
        """The bank is only in the commercial partner,
        and we are invoicing one of its contacts:
        the commercial partner's bank is set in the invoice.
        """
        # Arrange
        payment_term = self.payment_term1
        commercial_partner = self.env["res.partner"].create(
            {
                "name": "Test commercial partner",
                "bank_ids": [
                    Command.create(
                        {
                            "acc_number": "test account number",
                        }
                    ),
                ],
            }
        )
        bank = commercial_partner.bank_ids
        invoice_partner = self.env["res.partner"].create(
            {
                "name": "Test invoice partner",
                "parent_id": commercial_partner.id,
            }
        )
        # pre-condition
        self.assertFalse(invoice_partner.bank_ids)
        self.assertEqual(invoice_partner.parent_id, commercial_partner)
        self.assertTrue(bank)

        # Act
        move_form = Form(
            self.env["account.move"].with_context(
                default_move_type="out_invoice",
                default_name="Test invoice",
            )
        )
        move_form.partner_id = invoice_partner
        move_form.invoice_payment_term_id = payment_term
        move = move_form.save()

        # Assert
        self.assertEqual(move.riba_partner_bank_id, bank)
