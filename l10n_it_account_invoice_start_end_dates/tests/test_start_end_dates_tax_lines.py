# Copyright 2024 Lorenzo Battistini
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import date

from odoo import fields
from odoo.tests import Form, tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestStartEndDatesTaxLines(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Partially deductible VAT (50%): one repartition line with account_id
        # (deductible, goes to VAT credit account) and one without (non-deductible,
        # goes to expense account = cost for the company).
        cls.tax_partially_deductible = cls.env["account.tax"].create(
            {
                "name": "IVA 22% detraibile al 50%",
                "amount": 22,
                "amount_type": "percent",
                "type_tax_use": "purchase",
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
                            "factor_percent": 50,
                            "repartition_type": "tax",
                            "account_id": cls.company_data["default_account_assets"].id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 50,
                            "repartition_type": "tax",
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
                            "factor_percent": 50,
                            "repartition_type": "tax",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 50,
                            "repartition_type": "tax",
                            "account_id": cls.company_data["default_account_assets"].id,
                        },
                    ),
                ],
            }
        )
        # Totally non-deductible VAT: single repartition line without account_id.
        cls.tax_not_deductible = cls.env["account.tax"].create(
            {
                "name": "IVA 22% indetraibile",
                "amount": 22,
                "amount_type": "percent",
                "type_tax_use": "purchase",
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
                        },
                    ),
                ],
            }
        )
        # Fully deductible VAT (standard): repartition line with account_id.
        cls.tax_fully_deductible = cls.env["account.tax"].create(
            {
                "name": "IVA 22% detraibile",
                "amount": 22,
                "amount_type": "percent",
                "type_tax_use": "purchase",
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
                            "account_id": cls.company_data["default_account_assets"].id,
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
                            "account_id": cls.company_data["default_account_assets"].id,
                        },
                    ),
                ],
            }
        )
        cls.expense_account = cls.company_data["default_account_expense"]
        cls.start = date(2024, 1, 1)
        cls.end = date(2024, 12, 31)

    def _create_vendor_bill(self, tax, start_date=None, end_date=None):
        move_form = Form(
            self.env["account.move"].with_context(default_move_type="in_invoice")
        )
        move_form.partner_id = self.partner_a
        move_form.invoice_date = fields.Date.today()
        with move_form.invoice_line_ids.new() as line_form:
            line_form.name = "Test service"
            line_form.price_unit = 100
            line_form.account_id = self.expense_account
            line_form.tax_ids.clear()
            line_form.tax_ids.add(tax)
            if start_date:
                line_form.start_date = start_date
            if end_date:
                line_form.end_date = end_date
        return move_form.save()

    def test_partially_deductible_vat_propagates_dates(self):
        """Tax lines from partially deductible VAT (repartition without account_id)
        should inherit start/end dates from the invoice line."""
        bill = self._create_vendor_bill(
            self.tax_partially_deductible,
            start_date=self.start,
            end_date=self.end,
        )
        bill.action_post()
        # The tax line without account_id (non-deductible portion) goes to the
        # expense account and should have start/end dates.
        cost_tax_lines = bill.line_ids.filtered(
            lambda line: line.display_type == "tax"
            and line.tax_repartition_line_id
            and not line.tax_repartition_line_id.account_id
        )
        self.assertTrue(cost_tax_lines)
        for line in cost_tax_lines:
            self.assertEqual(line.start_date, self.start)
            self.assertEqual(line.end_date, self.end)
        # The tax line with account_id (deductible portion, VAT credit account)
        # should NOT have start/end dates.
        vat_credit_lines = bill.line_ids.filtered(
            lambda line: line.display_type == "tax"
            and line.tax_repartition_line_id
            and line.tax_repartition_line_id.account_id
        )
        self.assertTrue(vat_credit_lines)
        for line in vat_credit_lines:
            self.assertFalse(line.start_date)
            self.assertFalse(line.end_date)

    def test_totally_non_deductible_vat_propagates_dates(self):
        """Tax lines from totally non-deductible VAT (all repartition without
        account_id) should inherit start/end dates from the invoice line."""
        bill = self._create_vendor_bill(
            self.tax_not_deductible,
            start_date=self.start,
            end_date=self.end,
        )
        bill.action_post()
        cost_tax_lines = bill.line_ids.filtered(
            lambda line: line.display_type == "tax"
            and line.tax_repartition_line_id
            and not line.tax_repartition_line_id.account_id
        )
        self.assertTrue(cost_tax_lines)
        for line in cost_tax_lines:
            self.assertEqual(line.start_date, self.start)
            self.assertEqual(line.end_date, self.end)

    def test_fully_deductible_vat_no_dates(self):
        """Tax lines from fully deductible VAT (all repartition with account_id)
        should NOT get start/end dates."""
        bill = self._create_vendor_bill(
            self.tax_fully_deductible,
            start_date=self.start,
            end_date=self.end,
        )
        bill.action_post()
        tax_lines = bill.line_ids.filtered(lambda line: line.display_type == "tax")
        self.assertTrue(tax_lines)
        for line in tax_lines:
            self.assertFalse(line.start_date)
            self.assertFalse(line.end_date)

    def test_no_dates_on_invoice_line(self):
        """When invoice line has no dates, tax lines should not get dates either."""
        bill = self._create_vendor_bill(self.tax_partially_deductible)
        bill.action_post()
        tax_lines = bill.line_ids.filtered(lambda line: line.display_type == "tax")
        self.assertTrue(tax_lines)
        for line in tax_lines:
            self.assertFalse(line.start_date)
            self.assertFalse(line.end_date)

    def test_multiple_invoice_lines_different_dates(self):
        """Multiple invoice lines with different dates should create separate
        tax lines, each with their own dates."""
        start_1 = date(2024, 1, 1)
        end_1 = date(2024, 6, 30)
        start_2 = date(2024, 7, 1)
        end_2 = date(2024, 12, 31)
        move_form = Form(
            self.env["account.move"].with_context(default_move_type="in_invoice")
        )
        move_form.partner_id = self.partner_a
        move_form.invoice_date = fields.Date.today()
        with move_form.invoice_line_ids.new() as line_form:
            line_form.name = "Service H1"
            line_form.price_unit = 100
            line_form.account_id = self.expense_account
            line_form.tax_ids.clear()
            line_form.tax_ids.add(self.tax_partially_deductible)
            line_form.start_date = start_1
            line_form.end_date = end_1
        with move_form.invoice_line_ids.new() as line_form:
            line_form.name = "Service H2"
            line_form.price_unit = 200
            line_form.account_id = self.expense_account
            line_form.tax_ids.clear()
            line_form.tax_ids.add(self.tax_partially_deductible)
            line_form.start_date = start_2
            line_form.end_date = end_2
        bill = move_form.save()
        bill.action_post()
        cost_tax_lines = bill.line_ids.filtered(
            lambda line: line.display_type == "tax"
            and line.tax_repartition_line_id
            and not line.tax_repartition_line_id.account_id
        )
        # Two separate cost tax lines (one per date range).
        self.assertEqual(len(cost_tax_lines), 2)
        dates = cost_tax_lines.mapped(lambda line: (line.start_date, line.end_date))
        self.assertIn((start_1, end_1), dates)
        self.assertIn((start_2, end_2), dates)

    def test_dates_set_after_tax(self):
        """When dates are added after the invoice is saved with tax,
        tax lines should be recomputed and get the dates."""
        # Step 1: create bill with tax but no dates
        bill = self._create_vendor_bill(self.tax_partially_deductible)
        cost_tax_lines = bill.line_ids.filtered(
            lambda line: line.display_type == "tax"
            and line.tax_repartition_line_id
            and not line.tax_repartition_line_id.account_id
        )
        self.assertTrue(cost_tax_lines)
        for line in cost_tax_lines:
            self.assertFalse(line.start_date)
            self.assertFalse(line.end_date)

        # Step 2: edit the bill to add dates
        move_form = Form(bill)
        with move_form.invoice_line_ids.edit(0) as line_form:
            line_form.start_date = self.start
            line_form.end_date = self.end
        move_form.save()

        # Step 3: verify tax lines now have the dates
        cost_tax_lines = bill.line_ids.filtered(
            lambda line: line.display_type == "tax"
            and line.tax_repartition_line_id
            and not line.tax_repartition_line_id.account_id
        )
        self.assertTrue(cost_tax_lines)
        for line in cost_tax_lines:
            self.assertEqual(line.start_date, self.start)
            self.assertEqual(line.end_date, self.end)
