# Copyright 2025 Simone Rubino
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import datetime

from dateutil.relativedelta import relativedelta

from odoo.tests import Form, tagged
from odoo.tools.safe_eval import safe_eval

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestOpenTaxBalances(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.supplier_bill = cls.init_invoice(
            "in_invoice",
            invoice_date=datetime.date(2020, 6, 15),
            amounts=[
                100,
            ],
            taxes=cls.tax_sale_a,
            post=True,
        )

    def _get_wizard(self, from_date, to_date):
        """Create the wizard to show the Tax Balances."""
        wizard_form = Form(self.env["wizard.open.tax.balances"])
        wizard_form.from_date = from_date
        wizard_form.to_date = to_date
        wizard = wizard_form.save()
        return wizard

    def _get_tax_balances(self, from_date, to_date):
        """Get the Taxes shown by the wizard."""
        wizard = self._get_wizard(from_date, to_date)
        taxes_action = wizard.open_taxes()
        return (
            self.env[taxes_action["res_model"]]
            .with_context(**taxes_action["context"])
            .search(safe_eval(taxes_action["domain"]))
        )

    def test_wizard(self):
        """The settlement date is used in the Tax Balances."""
        # Arrange
        bill = self.supplier_bill
        bill_tax_amount = bill.amount_tax
        accounting_date = bill.date
        settlement_date = accounting_date + relativedelta(years=1)
        from_date = datetime.date(2021, 1, 1)
        to_date = datetime.date(2021, 12, 31)
        taxes = self._get_tax_balances(from_date, to_date)
        tax_balance = taxes.filtered(
            lambda tax, bill_tax=bill.line_ids.tax_ids: tax == bill_tax
        ).balance_regular
        # pre-condition
        self.assertTrue(bill_tax_amount)
        self.assertFalse(from_date <= accounting_date <= to_date)
        self.assertTrue(from_date <= settlement_date <= to_date)

        # Act
        bill.l10n_it_vat_settlement_date = settlement_date
        taxes = self._get_tax_balances(from_date, to_date)

        # Assert
        settled_tax_balance = taxes.filtered(
            lambda tax, bill_tax=bill.line_ids.tax_ids: tax == bill_tax
        ).balance_regular
        self.assertEqual(
            tax_balance - bill_tax_amount,
            settled_tax_balance,
            "Tax Balance hasn't changed "
            "when bill settlement date is out of the wizard range",
        )
