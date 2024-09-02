#  Copyright 2015 Agile Business Group <http://www.agilebg.com>
#  Copyright 2022 Simone Rubino - TAKOBI
#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import re

from odoo import fields
from odoo.tests import Form, tagged

from .common import TestVATStatementCommon


@tagged("post_install", "-at_install")
class TestTax(TestVATStatementCommon):
    def test_vat_statement(self):
        in_invoice_line_account = (
            self.env["account.account"]
            .search(
                [
                    (
                        "account_type",
                        "=",
                        "income",
                    )
                ],
                limit=1,
            )
            .id
        )

        out_invoice = self.invoice_model.create(
            {
                "invoice_date": self.recent_date,
                "journal_id": self.sale_journal.id,
                "partner_id": self.env.ref("base.res_partner_3").id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "service",
                            "price_unit": 100,
                            "quantity": 1,
                            "tax_ids": [(6, 0, [self.account_tax_22.id])],
                        },
                    )
                ],
            }
        )
        out_invoice.action_post()

        in_invoice = self.invoice_model.create(
            {
                "invoice_date": self.recent_date,
                "journal_id": self.purchase_journal.id,
                "partner_id": self.env.ref("base.res_partner_4").id,
                "move_type": "in_invoice",
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "service",
                            "account_id": in_invoice_line_account,
                            "price_unit": 50,
                            "quantity": 1,
                            "tax_ids": [(6, 0, [self.account_tax_22_credit.id])],
                        },
                    )
                ],
            }
        )
        in_invoice.action_post()

        last_year_in_invoice = self.invoice_model.create(
            {
                "invoice_date": self.last_year_recent_date,
                "journal_id": self.purchase_journal.id,
                "partner_id": self.env.ref("base.res_partner_4").id,
                "move_type": "in_invoice",
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "service",
                            "price_unit": 50,
                            "quantity": 1,
                            "tax_ids": [(6, 0, [self.account_tax_22_credit.id])],
                        },
                    )
                ],
            }
        )
        last_year_in_invoice.action_post()

        self.last_year_vat_statement = self.vat_statement_model.create(
            {
                "journal_id": self.general_journal.id,
                "authority_vat_account_id": self.vat_authority.id,
                "payment_term_id": self.account_payment_term.id,
                "date": self.last_year_date,
            }
        )
        self.last_year_period.vat_statement_id = self.last_year_vat_statement
        self.last_year_vat_statement.compute_amounts()

        self.vat_statement = self.vat_statement_model.create(
            {
                "journal_id": self.general_journal.id,
                "authority_vat_account_id": self.vat_authority.id,
                "payment_term_id": self.account_payment_term.id,
            }
        )
        self.current_period.vat_statement_id = self.vat_statement
        self.account_tax_22.invalidate_model()
        self.vat_statement.compute_amounts()
        self.vat_statement._compute_authority_vat_amount()
        self.vat_statement.previous_credit_vat_account_id = self.received_vat_account

        self.assertEqual(self.vat_statement.previous_credit_vat_amount, 11)
        self.assertTrue(self.vat_statement.previous_year_credit)
        self.assertEqual(self.vat_statement.authority_vat_amount, 0)
        self.assertEqual(self.vat_statement.deductible_vat_amount, 11)
        self.assertEqual(self.vat_statement.residual, 0)
        self.assertEqual(len(self.vat_statement.debit_vat_account_line_ids), 1)
        self.assertEqual(len(self.vat_statement.credit_vat_account_line_ids), 1)
        self.vat_statement.advance_account_id = self.paid_vat_account
        self.vat_statement.advance_amount = 100
        self.vat_statement._compute_authority_vat_amount()
        self.assertEqual(self.vat_statement.authority_vat_amount, -100)
        self.vat_statement.create_move()
        self.assertEqual(self.vat_statement.state, "confirmed")
        self.assertTrue(self.vat_statement.move_id)
        vat_auth_found = False
        for line in self.vat_statement.move_id.line_ids:
            if line.account_id.id == self.vat_statement.authority_vat_account_id.id:
                vat_auth_found = True
                self.assertEqual(line.debit, 100)
        self.assertTrue(vat_auth_found)
        # TODO payment

    def test_different_previous_vat_statements(self):
        """
        Statements for different Accounts
        only count previous Amounts from Statements with the same Accounts.
        """
        # Arrange: Create two different VAT Statements
        # selecting two different Accounts
        partner = self.env.ref("base.res_partner_4")
        tax = self.account_tax_22_credit
        tax_statement_account = tax.vat_statement_account_id
        last_year_bill = self._create_vendor_bill(
            partner,
            self.last_year_recent_date,
            10,
            tax,
        )
        self.assertEqual(last_year_bill.state, "posted")
        last_year_period = self.last_year_period
        last_year_statement = self._get_statement(
            last_year_period,
            self.last_year_date,
            tax_statement_account,
        )
        self.assertTrue(last_year_statement)

        # Create another Bill and Statement
        other_tax_statement_account = tax_statement_account.copy()
        other_tax = tax.copy(
            default={
                "vat_statement_account_id": other_tax_statement_account.id,
            },
        )
        other_last_year_bill = self._create_vendor_bill(
            partner,
            self.last_year_recent_date,
            20,
            other_tax,
        )
        self.assertEqual(other_last_year_bill.state, "posted")
        last_year_period.type_id.allow_overlap = True
        other_last_year_period = last_year_period.copy(
            default={
                "name": "Test Other last Year Period",
                "vat_statement_id": False,
            },
        )
        other_last_year_statement = self._get_statement(
            other_last_year_period,
            self.last_year_date,
            other_tax_statement_account,
        )
        self.assertTrue(other_last_year_statement)

        # Act: Create this Year's Statements,
        # one for each Account used in previous Statements
        today = fields.Date.today()
        current_period = self.current_period
        statement = self._get_statement(
            current_period,
            today,
            tax_statement_account,
        )

        current_period.type_id.allow_overlap = True
        other_current_period = current_period.copy(
            default={
                "name": "Test Other current Period",
                "vat_statement_id": False,
            },
        )
        other_statement = self._get_statement(
            other_current_period,
            today,
            other_tax_statement_account,
        )

        # Assert: Each one of this Year's Statements counts as previous Amount
        # only the corresponding last Year's Statement
        self.assertEqual(
            statement.previous_credit_vat_amount,
            -last_year_statement.authority_vat_amount,
        )
        self.assertEqual(
            other_statement.previous_credit_vat_amount,
            -other_last_year_statement.authority_vat_amount,
        )

    def test_create_move_with_payment_term(self):
        """When there is a payment term, the move can be created."""
        # Arrange
        date_range = self.current_period
        out_invoice = self.init_invoice(
            "out_invoice",
            invoice_date=self.recent_date,
            amounts=[
                100,
            ],
            taxes=self.account_tax_22,
            post=True,
        )
        statement = self._get_statement(
            date_range,
            self.last_year_date,
            self.env["account.account"].browse(),
            payment_term=self.env.ref("account.account_payment_term_advance_60days"),
        )
        # pre-condition
        self.assertTrue(statement.payment_term_id)
        self.assertIn(date_range, statement.date_range_ids)
        date_range_domain = date_range.get_domain("invoice_date")
        date_range_invoices = self.invoice_model.search(date_range_domain)
        self.assertIn(out_invoice, date_range_invoices)

        # Act
        statement.create_move()

        # Assert
        move = statement.move_id
        self.assertEqual(move.amount_total, 22)

    def test_report_multiple_payment_info(self):
        """
        If there are multiple payments for a statement,
        payment info is only printed once.
        """
        # Arrange
        tax = self.account_tax_22_credit
        tax_statement_account = tax.vat_statement_account_id
        last_year_bill = self.init_invoice(
            "in_invoice",
            invoice_date=self.last_year_recent_date,
            amounts=[100],
            taxes=tax,
            post=True,
        )
        self.assertEqual(last_year_bill.state, "posted")
        last_year_period = self.last_year_period
        self._get_statement(
            last_year_period,
            self.last_year_date,
            tax_statement_account,
        )

        date_range = self.current_period
        self.init_invoice(
            "out_invoice",
            invoice_date=self.recent_date,
            amounts=[
                1000,
            ],
            taxes=self.account_tax_22,
            post=True,
        )
        statement = self._get_statement(
            date_range,
            self.last_year_date,
            self.env["account.account"].browse(),
            payment_term=self.env.ref("account.account_payment_term_advance_60days"),
        )

        statement.create_move()
        move = statement.move_id

        reverse_action = move.action_reverse()
        reverse_wizard_form = Form(
            self.env[reverse_action["res_model"]].with_context(
                active_model=move._name,
                active_ids=move.ids,
            )
        )
        reverse_wizard = reverse_wizard_form.save()
        reverse_wizard.reverse_moves()
        # pre-condition
        self.assertEqual(len(statement.payment_ids), 2)

        # Act
        report_content, report_type = self.env["ir.actions.report"]._render_qweb_html(
            "account_vat_period_end_statement.report_vat_statement", statement.ids
        )

        # Assert
        payment_infos = re.findall(
            "Reverse charge: ",
            report_content.decode(),
        )
        self.assertEqual(len(payment_infos), 1)
