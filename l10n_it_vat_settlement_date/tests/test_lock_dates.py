#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import datetime

from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestLockDates(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.company = cls.env.company

    def test_bill_tax_lock(self):
        """The tax lock date is checked against
        the settlement date of a supplier bill."""
        settlement_date = datetime.date(2020, month=1, day=1)
        tax_lock_date = datetime.date(2020, month=1, day=2)
        accounting_date = datetime.date(2020, month=1, day=3)
        self.company.tax_lock_date = tax_lock_date
        bill = self.init_invoice(
            "in_invoice",
            invoice_date=accounting_date,
            amounts=[100],
        )
        # pre-condition
        self.assertEqual(bill.date, accounting_date)
        self.assertEqual(bill.invoice_date, accounting_date)
        self.assertTrue(settlement_date < tax_lock_date < accounting_date)
        self.assertFalse(bill.tax_lock_date_message)

        # Act
        bill.l10n_it_vat_settlement_date = settlement_date

        # Assert
        self.assertIn("VAT Settlement Date", bill.tax_lock_date_message)

    def test_invoice_tax_lock(self):
        """The tax lock date is checked against
        the settlement date of a customer invoice."""
        settlement_date = datetime.date(2020, month=1, day=1)
        tax_lock_date = datetime.date(2020, month=1, day=2)
        accounting_date = datetime.date(2020, month=1, day=3)
        self.company.tax_lock_date = tax_lock_date
        invoice = self.init_invoice(
            "out_invoice",
            invoice_date=accounting_date,
            amounts=[100],
        )
        # pre-condition
        self.assertEqual(invoice.date, accounting_date)
        self.assertEqual(invoice.invoice_date, accounting_date)
        self.assertTrue(settlement_date < tax_lock_date < accounting_date)
        self.assertFalse(invoice.tax_lock_date_message)

        # Act
        invoice.l10n_it_vat_settlement_date = settlement_date

        # Assert
        self.assertIn("VAT Settlement Date", invoice.tax_lock_date_message)
