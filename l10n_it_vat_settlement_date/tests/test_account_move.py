#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import datetime

from dateutil.relativedelta import relativedelta

from odoo.tests import Form, tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestAccountMove(AccountTestInvoicingCommon):
    def test_draft_not_readonly(self):
        """VAT settlement date is not readonly when invoice is in draft."""
        # Arrange
        bill = self.init_invoice(
            "in_invoice",
            invoice_date=datetime.date(2020, 1, 1),
            amounts=[
                100,
            ],
        )
        settlement_date = bill.invoice_date + relativedelta(days=1)
        # pre-condition
        self.assertEqual(bill.state, "draft")

        # Act
        with Form(bill) as bill_form:
            bill_form.l10n_it_vat_settlement_date = settlement_date

        # Assert
        self.assertEqual(bill.l10n_it_vat_settlement_date, settlement_date)

    def test_posted_readonly(self):
        """VAT settlement date is readonly when invoice is posted."""
        # Arrange
        bill = self.init_invoice(
            "in_invoice",
            invoice_date=datetime.date(2020, 1, 1),
            amounts=[
                100,
            ],
            post=True,
        )
        settlement_date = bill.invoice_date + relativedelta(days=1)
        # pre-condition
        self.assertEqual(bill.state, "posted")

        # Act
        with self.assertRaises(AssertionError) as ae:
            with Form(bill) as bill_form:
                bill_form.l10n_it_vat_settlement_date = settlement_date

        # Assert
        exc_message = ae.exception.args[0]
        self.assertIn("readonly field", exc_message)
        self.assertIn("l10n_it_vat_settlement_date", exc_message)
        self.assertNotEqual(bill.l10n_it_vat_settlement_date, settlement_date)
