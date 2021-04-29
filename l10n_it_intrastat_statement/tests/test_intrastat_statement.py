#  Copyright 2020 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import Form, TransactionCase


class TestIntrastatStatement(TransactionCase):
    def setUp(self):
        super().setUp()
        self.statement_model = self.env["account.intrastat.statement"]

        self.account_account_model = self.env["account.account"]
        self.account_account_receivable = self.account_account_model.create(
            {
                "code": "1",
                "name": "Debtors - (test)",
                "reconcile": True,
                "user_type_id": self.env.ref("account.data_account_type_receivable").id,
            }
        )
        self.account_account_payable = self.account_account_model.create(
            {
                "code": "2",
                "name": "Creditors - (test)",
                "reconcile": True,
                "user_type_id": self.env.ref("account.data_account_type_payable").id,
            }
        )

        self.tax22_purchase = self.env["account.tax"].create(
            {
                "name": "22% intra purchase",
                "description": "22",
                "amount": 22,
                "type_tax_use": "purchase",
            }
        )

        self.partner01 = self.env.ref("base.res_partner_1")
        self.partner01.update(
            {
                "vat": "IT02780790107",
                "property_account_receivable_id": self.account_account_receivable.id,
                "property_account_payable_id": self.account_account_payable.id,
            }
        )
        self.partner02 = self.env.ref("base.res_partner_2")
        self.partner02.update(
            {
                "vat": "IT12345670017",
                "property_account_receivable_id": self.account_account_receivable.id,
                "property_account_payable_id": self.account_account_payable.id,
            }
        )
        self.product01 = self.env.ref("product.product_product_10")
        self.service01 = self.env.ref("product.product_product_1")
        self.service01.update(
            {
                "intrastat_type": "service",
                "intrastat_code_id": self.env.ref(
                    "l10n_it_intrastat.intrastat_intrastat_01012100"
                ),
            }
        )
        # Demo tax is in another company than current user's company.
        # We can't change this tax's company because
        # it is the default sale tax for the company
        # and it has already been used in other invoices.
        self.tax22_sale = (
            self.env.ref("l10n_it_intrastat.tax_22")
            .sudo()
            .copy(default={"company_id": self.env.company.id})
        )
        self.currency_gbp = self.env.ref("base.GBP")

        company = self.env.company
        company.partner_id.vat = "IT03339130126"
        company.intrastat_custom_id = self.env.ref("l10n_it_intrastat.014100")
        company.intrastat_purchase_transaction_nature_id = self.env.ref(
            "l10n_it_intrastat.code_8"
        )
        company.intrastat_sale_transaction_nature_id = self.env.ref(
            "l10n_it_intrastat.code_9"
        )

    def _get_intrastat_computed_bill(
        self, product=None, currency=None, price_unit=100.0
    ):
        if product is None:
            product = self.product01
        invoice = self._create_move(
            "in_invoice",
            partner=self.partner01,
            product=product,
            taxes=self.tax22_purchase,
            amount=price_unit,
        )
        if currency:
            invoice.currency_id = currency
        invoice.action_post()
        return invoice

    def _get_intrastat_computed_invoice(self, price_unit=100.0):
        invoice = self._create_move(
            "out_invoice",
            partner=self.partner01,
            product=self.product01,
            taxes=self.tax22_sale,
            amount=price_unit,
            post=True,
        )
        return invoice

    def test_statement_sale(self):
        invoice = self._get_intrastat_computed_invoice()

        statement = self.statement_model.create(
            {
                "period_number": invoice.invoice_date.month,
                "fiscalyear": invoice.invoice_date.year,
            }
        )

        # Check that before computation, file generation raises an exception
        # because statement is still empty
        with self.assertRaises(ValidationError):
            statement.generate_file_export()

        statement.compute_statement()
        file_content = statement.with_context(sale=True).generate_file_export()
        self.assertIn(invoice.partner_id.vat[2:], file_content)

        # Last line is section line, for monthly report it should be 103 chars
        self.assertEqual(len(file_content.splitlines()[-1]), 103)

    def test_statement_sale_quarter(self):
        invoice = self._get_intrastat_computed_invoice()
        month = invoice.invoice_date.month
        quarter = 1 + (month - 1) // 3
        statement = self.statement_model.create(
            {
                "period_number": quarter,
                "period_type": "T",
                "fiscalyear": invoice.invoice_date.year,
            }
        )

        statement.compute_statement()
        file_content = statement.with_context(sale=True).generate_file_export()
        self.assertIn(invoice.partner_id.vat[2:], file_content)

        # Last line is section line, for quarter report it should be 64 chars
        self.assertEqual(len(file_content.splitlines()[-1]), 64)

    def test_statement_purchase(self):
        bill = self._get_intrastat_computed_bill()

        statement = self.statement_model.create(
            {
                "period_number": bill.invoice_date.month,
                "fiscalyear": bill.invoice_date.year,
            }
        )

        # Check that before computation, file generation raises an exception
        # because statement is still empty
        with self.assertRaises(ValidationError):
            statement.generate_file_export()

        statement.compute_statement()
        file_content = statement.with_context(purchase=True).generate_file_export()
        self.assertIn(bill.partner_id.vat[2:], file_content)

        # Last line is section line, for monthly report it should be 118 chars
        self.assertEqual(len(file_content.splitlines()[-1]), 118)

    def test_statement_purchase_currency(self):
        bill = self._get_intrastat_computed_bill(currency=self.currency_gbp)

        statement = self.statement_model.create(
            {
                "period_number": bill.invoice_date.month,
                "fiscalyear": bill.invoice_date.year,
            }
        )

        statement.compute_statement()
        line = statement.purchase_section1_ids.filtered(lambda l: l.invoice_id == bill)
        self.assertEqual(bill.intrastat_line_ids.amount_currency, line.amount_currency)

    def test_statement_purchase_refund(self):
        bill = self._get_intrastat_computed_bill()

        bill_refund = self._create_move_refund(bill)
        # This refund will be subtracted from bill
        bill_refund.update(
            {
                "intrastat": True,
            }
        )
        bill_refund.action_post()
        bill_refund.compute_intrastat_lines()

        statement = self.statement_model.create(
            {
                "period_number": bill_refund.invoice_date.month,
                "fiscalyear": bill_refund.invoice_date.year,
            }
        )

        # Check that before computation, file generation raises an exception
        # because statement is still empty
        with self.assertRaises(ValidationError):
            statement.generate_file_export()

        statement.compute_statement()
        file_content = statement.with_context(purchase=True).generate_file_export()
        self.assertIn(bill_refund.partner_id.vat[2:], file_content)

        # Monthly Purchase file lengths
        # File head line: 75
        # Frontispiece: 130
        # Goods bill: 118
        file_lines = file_content.splitlines()
        self.assertEqual(len(file_lines), 3)
        self.assertSetEqual({len(line) for line in file_lines}, {75, 130, 118})

    def test_statement_purchase_refund_no_subtract(self):
        bill = self._get_intrastat_computed_bill()

        bill_refund = self._create_move_refund(bill)

        # Change the partner so that this refund is not subtracted from bill
        bill_refund.update(
            {
                "partner_id": self.partner02.id,
                "intrastat": True,
            }
        )
        bill_refund.action_post()
        bill_refund.compute_intrastat_lines()

        statement = self.statement_model.create(
            {
                "period_number": bill_refund.invoice_date.month,
                "fiscalyear": bill_refund.invoice_date.year,
            }
        )

        # Check that before computation, file generation raises an exception
        # because statement is still empty
        with self.assertRaises(ValidationError):
            statement.generate_file_export()

        statement.compute_statement()
        file_content = statement.with_context(purchase=True).generate_file_export()
        self.assertIn(bill_refund.partner_id.vat[2:], file_content)

        # Monthly Purchase file lengths
        # File head line: 75
        # Frontispiece: 130
        # Goods bill: 118
        # Goods refund: 96
        file_lines = file_content.splitlines()
        self.assertEqual(len(file_lines), 4)
        self.assertSetEqual({len(line) for line in file_lines}, {75, 130, 118, 96})

    def test_statement_purchase_service_refund_no_subtract(self):
        bill = self._get_intrastat_computed_bill(self.service01)

        bill_refund = self._create_move_refund(bill)
        # Change the partner so that this refund is not subtracted from bill
        bill_refund.update(
            {
                "partner_id": self.partner02.id,
                "intrastat": True,
            }
        )
        bill_refund.action_post()
        bill_refund.compute_intrastat_lines()

        statement = self.statement_model.create(
            {
                "period_number": bill_refund.invoice_date.month,
                "fiscalyear": bill_refund.invoice_date.year,
            }
        )

        # Check that before computation, file generation raises an exception
        # because statement is still empty
        with self.assertRaises(ValidationError):
            statement.generate_file_export()

        statement.compute_statement()
        # When there are refund lines, fields
        # protocol number and progressive to modify must be provided
        with self.assertRaises(ValidationError):
            statement.with_context(purchase=True).generate_file_export()

        statement.purchase_section4_ids.update(
            {
                "protocol": 123456,
                "progressive_to_modify": 1,
            }
        )
        file_content = statement.with_context(purchase=True).generate_file_export()
        self.assertIn(bill_refund.partner_id.vat[2:], file_content)

        # Monthly Purchase file lengths
        # File head line: 75
        # Frontispiece: 130
        # Services bill: 99
        # Services refund: 118
        file_lines = file_content.splitlines()
        self.assertEqual(len(file_lines), 4)
        self.assertEqual(len(file_lines[0]), 75)
        self.assertEqual(len(file_lines[1]), 130)
        self.assertSetEqual({len(line) for line in file_lines[2:]}, {99, 118})

    def test_statement_purchase_quarter(self):
        bill = self._get_intrastat_computed_bill()
        month = bill.invoice_date.month
        quarter = 1 + (month - 1) // 3
        statement = self.statement_model.create(
            {
                "period_number": quarter,
                "period_type": "T",
                "fiscalyear": bill.invoice_date.year,
            }
        )

        statement.compute_statement()
        file_content = statement.with_context(purchase=True).generate_file_export()
        self.assertIn(bill.partner_id.vat[2:], file_content)

        # Last line is section line, for quarter report it should be 77 chars
        self.assertEqual(len(file_content.splitlines()[-1]), 77)

    def test_statement_export_file(self):
        invoice = self._get_intrastat_computed_invoice()

        statement = self.statement_model.create(
            {
                "period_number": invoice.invoice_date.month,
                "fiscalyear": invoice.invoice_date.year,
            }
        )
        statement.compute_statement()

        export_wizard = (
            self.env["account.intrastat.export.file"]
            .with_context(active_id=statement.id, sale=True)
            .create({})
        )
        export_wizard.act_getfile()
        file_content = base64.decodebytes(export_wizard.data)
        self.assertIn(invoice.partner_id.vat[2:], str(file_content))

    def test_purchase_default_transaction_nature(self):
        """Check default value for purchase's transaction nature."""
        bill = self._get_intrastat_computed_bill()

        statement = self.statement_model.create(
            {
                "period_number": bill.invoice_date.month,
                "fiscalyear": bill.invoice_date.year,
            }
        )
        line = statement.purchase_section1_ids.create({})
        company = self.env.company
        self.assertEqual(
            company.intrastat_purchase_transaction_nature_id, line.transaction_nature_id
        )

    def test_sale_default_transaction_nature(self):
        """Check default value for sale's transaction nature."""
        invoice = self._get_intrastat_computed_invoice()

        statement = self.statement_model.create(
            {
                "period_number": invoice.invoice_date.month,
                "fiscalyear": invoice.invoice_date.year,
            }
        )

        line = statement.sale_section1_ids.create({})
        company = self.env.company
        self.assertEqual(
            company.intrastat_sale_transaction_nature_id, line.transaction_nature_id
        )

    def test_statement_sale_round_up_amounts(self):
        """
        Check that amount_euro and statistic_amount_euro are rounded up.
        """
        invoice = self._get_intrastat_computed_invoice(price_unit=100.5)

        statement = self.statement_model.create(
            {
                "period_number": invoice.invoice_date.month,
                "fiscalyear": invoice.invoice_date.year,
            }
        )
        statement.compute_statement()
        statement_invoice_line = statement.sale_section1_ids.filtered(
            lambda l: l.invoice_id == invoice
        )
        self.assertEqual(statement_invoice_line.amount_euro, 101)
        self.assertEqual(statement_invoice_line.statistic_amount_euro, 101)

    def test_statement_sale_round_down_amounts(self):
        """
        Check that amount_euro and statistic_amount_euro are rounded down.
        """
        invoice = self._get_intrastat_computed_invoice(price_unit=100.4)

        statement = self.statement_model.create(
            {
                "period_number": invoice.invoice_date.month,
                "fiscalyear": invoice.invoice_date.year,
            }
        )
        statement.compute_statement()
        statement_invoice_line = statement.sale_section1_ids.filtered(
            lambda l: l.invoice_id == invoice
        )
        self.assertEqual(statement_invoice_line.amount_euro, 100)
        self.assertEqual(statement_invoice_line.statistic_amount_euro, 100)

    def test_statement_purchase_round_up_amounts(self):
        """
        Check that amount_euro and statistic_amount_euro are rounded up,
        but amount_currency is truncated.
        """
        bill = self._get_intrastat_computed_bill(
            currency=self.currency_gbp,
            price_unit=100.4,
        )

        statement = self.statement_model.create(
            {
                "period_number": bill.invoice_date.month,
                "fiscalyear": bill.invoice_date.year,
            }
        )
        statement.compute_statement()
        statement_invoice_line = statement.purchase_section1_ids.filtered(
            lambda l: l.invoice_id == bill
        )

        bill_amount_euro = bill.intrastat_line_ids.amount_euro
        self.assertEqual(
            statement_invoice_line.amount_euro, int(round(bill_amount_euro))
        )
        self.assertEqual(
            statement_invoice_line.statistic_amount_euro, int(round(bill_amount_euro))
        )

        amount_currency = int(bill.intrastat_line_ids.amount_currency)
        self.assertEqual(statement_invoice_line.amount_currency, amount_currency)

    def test_statement_purchase_round_down_amounts(self):
        """
        Check that amount_euro and statistic_amount_euro are rounded down,
        but amount_currency is truncated.
        """
        bill = self._get_intrastat_computed_bill(
            currency=self.currency_gbp,
            price_unit=100.4,
        )

        statement = self.statement_model.create(
            {
                "period_number": bill.invoice_date.month,
                "fiscalyear": bill.invoice_date.year,
            }
        )
        statement.compute_statement()
        statement_invoice_line = statement.purchase_section1_ids.filtered(
            lambda l: l.invoice_id == bill
        )

        bill_amount_euro = bill.intrastat_line_ids.amount_euro
        self.assertEqual(
            statement_invoice_line.amount_euro, int(round(bill_amount_euro))
        )
        self.assertEqual(
            statement_invoice_line.statistic_amount_euro, int(round(bill_amount_euro))
        )

        amount_currency = int(bill.intrastat_line_ids.amount_currency)
        self.assertEqual(statement_invoice_line.amount_currency, amount_currency)

    def _create_move(
        self,
        move_type,
        partner=None,
        invoice_date=None,
        post=False,
        product=None,
        amount=None,
        taxes=None,
    ):
        move_form = Form(
            self.env["account.move"].with_context(default_move_type=move_type)
        )
        move_form.invoice_date = invoice_date or fields.Date.from_string("2019-01-01")
        move_form.partner_id = partner or self.partner_a
        move_form.intrastat = True

        with move_form.invoice_line_ids.new() as line_form:
            line_form.product_id = product
            line_form.price_unit = amount
            if taxes:
                line_form.tax_ids.clear()
                line_form.tax_ids.add(taxes)

        rslt = move_form.save()

        if post:
            rslt.action_post()

        return rslt

    def _create_move_refund(self, move):
        move_reversal = (
            self.env["account.move.reversal"]
            .with_context(active_model="account.move", active_ids=move.ids)
            .create(
                {
                    "date": fields.Date.from_string("2019-01-01"),
                    "reason": "no reason",
                    "refund_method": "refund",
                }
            )
        )
        reversal = move_reversal.reverse_moves()
        move_refund = self.env["account.move"].browse(reversal["res_id"])
        return move_refund
