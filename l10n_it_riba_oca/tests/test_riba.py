# Author: Andrea Gallina
# ©  2015 Apulia Software srl
# Copyright (C) 2017 Lorenzo Battistini - Agile Business Group
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
import datetime
import os

from odoo import Command
from odoo.exceptions import UserError
from odoo.fields import first
from odoo.tests import Form
from odoo.tools import config, safe_eval

from . import riba_common


class TestInvoiceDueCost(riba_common.TestRibaCommon):
    def test_add_due_cost(self):
        # ---- Set Service in Company Config
        self.invoice.company_id.due_cost_service_id = self.service_due_cost.id
        # ---- Validate Invoice
        self.invoice.action_post()
        # ---- Test Invoice has 2 line
        self.assertEqual(len(self.invoice.invoice_line_ids), 3)
        # ---- Test Invoice Line for service cost
        self.assertEqual(
            self.invoice.invoice_line_ids[1].product_id.id, self.service_due_cost.id
        )
        # ---- Test Invoice Line for service cost
        self.assertEqual(
            self.invoice.invoice_line_ids[2].product_id.id, self.service_due_cost.id
        )
        # ---- Test Cost line is equal to 10.00
        self.assertEqual(
            (
                self.invoice.invoice_line_ids[1].price_unit
                + self.invoice.invoice_line_ids[2].price_unit
            ),
            10.00,
        )
        new_inv = self.invoice.copy()
        self.assertEqual(len(new_inv.invoice_line_ids), 1)

    def test_not_add_due_cost(self):
        # create 2 invoice for partner in same month on the second one no
        # collection fees line expected
        # ---- Set Service in Company Config
        self.invoice.company_id.due_cost_service_id = self.service_due_cost.id
        # ---- Validate Invoice
        self.invoice.action_post()

        self.invoice2.invoice_payment_term_id = self.payment_term2
        self.invoice2.action_post()
        # ---- Test Invoice has 1 line, no collection fees added because it's added on
        # ---- first due date for partner
        self.assertEqual(len(self.invoice2.invoice_line_ids), 1)

    def test_delete_due_cost_line(self):
        # ---- Set Service in Company Config
        self.invoice.company_id.due_cost_service_id = self.service_due_cost.id
        # ---- Validate Invoice
        self.invoice.action_post()
        # ---- Cancel Invoice
        self.invoice.button_cancel()
        self.invoice.button_draft()
        # ---- Set to Draft
        # Collection fees line has been unlink
        self.assertEqual(len(self.invoice.invoice_line_ids), 1)

    def riba_sbf_common(self):
        invoice = self._create_sbf_invoice()
        invoice._onchange_riba_partner_bank_id()
        invoice.action_post()
        riba_move_line_id = False
        for move_line in invoice.line_ids:
            if move_line.account_id.id == self.account_rec1_id.id:
                riba_move_line_id = move_line.id
                line_ids = self.move_line_model.search(
                    [
                        "&",
                        "|",
                        ("riba", "=", "True"),
                        ("past_due_invoice_ids", "!=", False),
                        ("account_type", "=", "asset_receivable"),
                        ("reconciled", "=", False),
                        ("slip_line_ids", "=", False),
                        ("move_id", "=", invoice.id),
                    ]
                )
                self.assertEqual(len(line_ids), 1)
                self.assertEqual(line_ids[0].id, move_line.id)
        self.assertTrue(riba_move_line_id)

        # issue wizard
        wizard_riba_issue = self.env["riba.issue"].create(
            {"configuration_id": self.riba_config_sbf.id}
        )
        action = wizard_riba_issue.with_context(
            active_ids=[riba_move_line_id]
        ).create_list()
        riba_list_id = action and action["res_id"] or False
        riba_list = self.slip_model.browse(riba_list_id)
        riba_list.confirm()
        self.assertEqual(riba_list.state, "accepted")
        self.assertEqual(invoice.state, "posted")

        # Se la compute non viene invocata il test fallisce
        riba_list._compute_acceptance_move_ids()
        self.assertEqual(len(riba_list.acceptance_move_ids), 1)
        # Check that no payments exist yet
        self.assertEqual(len(riba_list.payment_ids), 0)

        # I print the RiBa slip report
        docargs = {
            "doc_ids": riba_list.ids,
            "doc_model": "riba.slip",
            "docs": self.env["riba.slip"].browse(riba_list.ids),
        }
        data = self.env["ir.qweb"]._render("l10n_it_riba_oca.slip_qweb", docargs)
        if config.get("test_report_directory"):
            open(
                os.path.join(config["test_report_directory"], "riba-list." + format),
                "wb+",
            ).write(data)

        # credit wizard
        credit_wizard = (
            self.env["riba.credit"]
            .with_context(
                active_model="riba.slip",
                active_ids=[riba_list_id],
                active_id=riba_list_id,
            )
            .create(
                {
                    "credit_amount": 450,
                    "expense_amount": 5,
                }
            )
        )
        res = credit_wizard.create_move()
        credit_move_id = self.env["account.move"].browse(res["res_id"])
        credit_move_id.action_post()
        self.assertEqual(riba_list.state, "credited")

        # Test that credit_move_id is properly set on riba lines
        for line in riba_list.line_ids:
            self.assertEqual(line.credit_move_id, riba_list.credit_move_id)
            self.assertTrue(
                line.credit_move_id, "RiBa line should have credit_move_id set"
            )

        return invoice, riba_list

    def test_riba_sbf_flow(self):
        invoice, riba_list = self.riba_sbf_common()

        # past due wizard
        past_due_wizard = (
            self.env["riba.past_due"]
            .with_context(
                active_model="riba.slip.line",
                active_ids=[riba_list.line_ids[0].id],
                active_id=riba_list.line_ids[0].id,
            )
            .create(
                {
                    "past_due_fee_amount": 5,
                }
            )
        )
        past_due_wizard.create_move()
        self.assertEqual(riba_list.state, "past_due")
        self.assertEqual(len(riba_list.line_ids), 1)
        self.assertEqual(riba_list.line_ids[0].state, "past_due")
        self.assertTrue(invoice.past_due_move_line_ids)

        # Se la compute non viene invocata il test fallisce
        riba_list._compute_past_due_move_ids()
        self.assertEqual(len(riba_list.past_due_move_ids), 1)
        bank_past_due_line = False
        for past_due_line in riba_list.past_due_move_ids[0].line_ids:
            if past_due_line.account_id.id == self.past_due_account.id:
                bank_past_due_line = past_due_line
                break
        self.assertTrue(bank_past_due_line)

    def test_riba_incasso_all_paid(self):
        """
        RiBa of type 'After Collection' all paid flow
        """
        self.invoice.company_id.due_cost_service_id = self.service_due_cost
        self.invoice.action_post()
        self.assertEqual(self.invoice.state, "posted")

        to_issue_action = self.env.ref("l10n_it_riba_oca.action_riba_to_issue")
        to_issue_model = self.env[to_issue_action.res_model]
        to_issue_domain = safe_eval.safe_eval(to_issue_action.domain)
        to_issue_records = (
            to_issue_model.search(to_issue_domain) & self.invoice.line_ids
        )
        self.assertTrue(to_issue_records)

        issue_wizard_context = {
            "active_model": to_issue_records._name,
            "active_ids": to_issue_records.ids,
        }
        issue_wizard_model = self.env["riba.issue"].with_context(**issue_wizard_context)
        issue_wizard_form = Form(issue_wizard_model)
        issue_wizard_form.configuration_id = self.riba_config_incasso
        issue_wizard = issue_wizard_form.save()
        issue_result = issue_wizard.create_list()

        riba_list_id = issue_result["res_id"]
        riba_list_model = issue_result["res_model"]
        riba_list = self.env[riba_list_model].browse(riba_list_id)
        riba_list.confirm()

        self.assertEqual(riba_list.state, "accepted")
        self.assertEqual(self.invoice.state, "posted")

        # invoice should be paid
        self.assertEqual(self.invoice.payment_state, "paid")

        # Action: Pay the RiBa
        payment_wizard_action = riba_list.settle_all_line()
        payment_wizard_form = Form(
            self.env[payment_wizard_action["res_model"]].with_context(
                **payment_wizard_action["context"]
            )
        )
        # payment_wizard_form.payment_date = datetime.date.today()
        payment_wizard = payment_wizard_form.save()
        payment_wizard.pay()

        # Assert
        self.assertEqual(riba_list.state, "paid")
        # invoice should be partial paid
        self.assertEqual(self.invoice.payment_state, "paid")

    def test_riba_incasso_past_due(self):
        """
        RiBa of type 'After Collection' past due flow
        """
        self.invoice.company_id.due_cost_service_id = self.service_due_cost
        self.invoice.action_post()
        self.assertEqual(self.invoice.state, "posted")

        to_issue_action = self.env.ref("l10n_it_riba_oca.action_riba_to_issue")
        to_issue_model = self.env[to_issue_action.res_model]
        to_issue_domain = safe_eval.safe_eval(to_issue_action.domain)
        to_issue_records = (
            to_issue_model.search(to_issue_domain) & self.invoice.line_ids
        )
        self.assertTrue(to_issue_records)

        issue_wizard_context = {
            "active_model": to_issue_records._name,
            "active_ids": to_issue_records.ids,
        }
        issue_wizard_model = self.env["riba.issue"].with_context(**issue_wizard_context)
        issue_wizard_form = Form(issue_wizard_model)
        issue_wizard_form.configuration_id = self.riba_config_incasso
        issue_wizard = issue_wizard_form.save()
        issue_result = issue_wizard.create_list()

        riba_list_id = issue_result["res_id"]
        riba_list_model = issue_result["res_model"]
        riba_list = self.env[riba_list_model].browse(riba_list_id)
        riba_list.confirm()

        self.assertEqual(riba_list.state, "accepted")
        self.assertEqual(self.invoice.state, "posted")

        # invoice should be paid
        self.assertEqual(self.invoice.payment_state, "paid")

        # past due wizard
        past_due_wizard = (
            self.env["riba.past_due"]
            .with_context(
                active_model="riba.slip.line",
                active_ids=[riba_list.line_ids[0].id],
                active_id=riba_list.line_ids[0].id,
            )
            .create({})
        )
        past_due_wizard.create_move()
        self.assertEqual(riba_list.state, "past_due")
        self.assertEqual(len(riba_list.line_ids), 2)
        self.assertEqual(riba_list.line_ids[0].state, "past_due")
        self.assertTrue(self.invoice.past_due_move_line_ids)
        # invoice should be partial paid
        self.assertEqual(self.invoice.payment_state, "partial")

    def test_past_due_riba(self):
        """
        RiBa of type 'sbf' past due flow
        """
        self.partner.property_account_receivable_id = self.account_rec1_id.id
        recent_date = (
            self.env["account.move"]
            .search([("invoice_date", "!=", False)], order="invoice_date desc", limit=1)
            .invoice_date
        )
        invoice = self.env["account.move"].create(
            {
                "invoice_date": recent_date,
                "move_type": "out_invoice",
                "journal_id": self.sale_journal.id,
                "partner_id": self.partner.id,
                "invoice_payment_term_id": self.account_payment_term_riba.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "product1",
                            "product_id": self.product1.id,
                            "quantity": 1.0,
                            "price_unit": 100.00,
                            "account_id": self.sale_account.id,
                            "tax_ids": [[6, 0, []]],
                        },
                    )
                ],
            }
        )
        invoice._onchange_riba_partner_bank_id()
        invoice.action_post()
        for move_line in invoice.line_ids:
            if move_line.account_id.id == self.account_rec1_id.id:
                riba_move_line_id = move_line.id
        # issue wizard
        wizard_riba_issue = self.env["riba.issue"].create(
            {"configuration_id": self.riba_config_sbf.id}
        )
        action = wizard_riba_issue.with_context(
            active_ids=[riba_move_line_id]
        ).create_list()
        riba_list_id = action and action["res_id"] or False
        riba_list = self.slip_model.browse(riba_list_id)
        riba_list.confirm()
        self.assertEqual(riba_list.state, "accepted")
        self.assertEqual(invoice.state, "posted")
        # credit wizard
        credit_wizard = (
            self.env["riba.credit"]
            .with_context(
                active_model="riba.slip",
                active_ids=[riba_list_id],
                active_id=riba_list_id,
            )
            .create(
                {
                    "credit_amount": 100,
                    "expense_amount": 5,
                }
            )
        )

        res = credit_wizard.create_move()
        credit_move_id = self.env["account.move"].browse(res["res_id"])
        credit_move_id.action_post()
        self.assertEqual(riba_list.state, "credited")

        # pay wizard with skip
        payment_wizard = (
            self.env["riba.payment.multiple"]
            .with_context(
                active_model="riba.slip",
                active_ids=[riba_list_id],
                active_id=riba_list_id,
            )
            .create({})
        )
        payment_wizard.skip()
        self.assertEqual(riba_list.state, "paid")
        self.assertEqual(riba_list.line_ids[0].state, "paid")

        # past due wizard
        past_due_wizard = (
            self.env["riba.past_due"]
            .with_context(
                active_model="riba.slip.line",
                active_ids=[riba_list.line_ids[0].id],
                active_id=riba_list.line_ids[0].id,
            )
            .create(
                {
                    "overdue_credit_amount": 100,
                    "past_due_fee_amount": 2,
                }
            )
        )
        past_due_wizard.create_move()
        self.assertEqual(riba_list.state, "past_due")
        self.assertEqual(len(riba_list.line_ids), 1)
        self.assertEqual(riba_list.line_ids[0].state, "past_due")
        self.assertTrue(invoice.past_due_move_line_ids)

        # Se la compute non viene invocata il test fallisce
        riba_list._compute_past_due_move_ids()
        self.assertEqual(len(riba_list.past_due_move_ids), 1)
        bank_past_due_line = False
        for past_due_line in riba_list.past_due_move_ids[0].line_ids:
            if past_due_line.account_id.id == self.riba_account.id:
                bank_past_due_line = past_due_line
                break
        self.assertTrue(bank_past_due_line)

        # register the bank statement with the bank credit
        # st = self.env['account.bank.statement'].create({
        #     'journal_id': self.bank_journal.id,
        #     'name': 'bank statement',
        #     'line_ids': [(0, 0, {
        #         'name': 'RiBa',
        #         'amount': -102,
        #     })]
        # })
        # must be possible to close the bank statement line with the
        # past due journal item generated by RiBa
        # move_lines_for_rec=st.line_ids[0].get_move_lines_for_reconciliation()
        # self.assertTrue(
        #     bank_past_due_line.id in [l.id for l in move_lines_for_rec])

    def test_riba_fatturapa(self):
        self.partner.property_account_receivable_id = self.account_rec1_id.id
        recent_date = (
            self.env["account.move"]
            .search([("invoice_date", "!=", False)], order="invoice_date desc", limit=1)
            .invoice_date
        )
        invoice = self.env["account.move"].create(
            {
                "invoice_date": recent_date,
                "move_type": "out_invoice",
                "journal_id": self.sale_journal.id,
                "partner_id": self.partner.id,
                "invoice_payment_term_id": self.account_payment_term_riba.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "product1",
                            "product_id": self.product1.id,
                            "quantity": 1.0,
                            "price_unit": 450.00,
                            "account_id": self.sale_account.id,
                            "tax_ids": [[6, 0, self.tax_22.ids]],
                        },
                    )
                ],
            }
        )
        invoice._onchange_riba_partner_bank_id()
        invoice.action_post()
        # issue wizard
        riba_move_line_id = invoice.line_ids.filtered(
            lambda x: x.account_id == self.account_rec1_id
        )
        wizard_riba_issue = self.env["riba.issue"].create(
            {"configuration_id": self.riba_config_sbf.id}
        )
        action = wizard_riba_issue.with_context(
            active_ids=[riba_move_line_id.id]
        ).create_list()
        riba_list_id = action and action["res_id"] or False
        riba_list = self.slip_model.browse(riba_list_id)
        riba_list.confirm()
        wizard_riba_export = self.env["riba.file.export"].create({})
        wizard_riba_export.with_context(active_ids=[riba_list.id]).act_getfile()
        # Assert
        file_content = base64.decodebytes(wizard_riba_export.riba_txt).decode()
        self.assertNotIn("INV/2025/00004", file_content)
        self.assertIn("CABNP Paribas", file_content)

    def test_riba_fatturapa_group(self):
        self.partner.group_riba = True
        self.partner.property_account_receivable_id = self.account_rec1_id.id
        recent_date = (
            self.env["account.move"]
            .search([("invoice_date", "!=", False)], order="invoice_date desc", limit=1)
            .invoice_date
        )
        invoice = self.env["account.move"].create(
            {
                "invoice_date": recent_date,
                "move_type": "out_invoice",
                "journal_id": self.sale_journal.id,
                "partner_id": self.partner.id,
                "invoice_payment_term_id": self.account_payment_term_riba.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "product1",
                            "product_id": self.product1.id,
                            "quantity": 1.0,
                            "price_unit": 450.00,
                            "account_id": self.sale_account.id,
                            "tax_ids": [[6, 0, self.tax_22.ids]],
                        },
                    )
                ],
            }
        )
        invoice._onchange_riba_partner_bank_id()
        invoice.action_post()
        invoice1 = self.env["account.move"].create(
            {
                "invoice_date": recent_date,
                "move_type": "out_invoice",
                "journal_id": self.sale_journal.id,
                "partner_id": self.partner.id,
                "invoice_payment_term_id": self.account_payment_term_riba.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "product1",
                            "product_id": self.product1.id,
                            "quantity": 1.0,
                            "price_unit": 450.00,
                            "account_id": self.sale_account.id,
                            "tax_ids": [[6, 0, self.tax_22.ids]],
                        },
                    )
                ],
            }
        )
        invoice1._onchange_riba_partner_bank_id()
        invoice1.action_post()
        # issue wizard
        riba_move_line_id = invoice.line_ids.filtered(
            lambda x: x.account_id == self.account_rec1_id
        )
        riba_move_line1_id = invoice1.line_ids.filtered(
            lambda x: x.account_id == self.account_rec1_id
        )
        wizard_riba_issue = self.env["riba.issue"].create(
            {"configuration_id": self.riba_config_sbf.id}
        )
        action = wizard_riba_issue.with_context(
            active_ids=[riba_move_line_id.id, riba_move_line1_id.id]
        ).create_list()
        riba_list_id = action and action["res_id"] or False
        riba_list = self.slip_model.browse(riba_list_id)
        riba_list.confirm()
        self.assertTrue(len(riba_list.line_ids), 2)
        wizard_riba_export = self.env["riba.file.export"].create({})
        wizard_riba_export.with_context(active_ids=[riba_list.id]).act_getfile()
        # Assert
        file_content = base64.decodebytes(wizard_riba_export.riba_txt).decode()
        self.assertNotIn("INV/2025/00008", file_content)
        self.assertIn("INV/2025/00005", file_content)
        self.assertIn("INV/2025/00006", file_content)

    def test_riba_presentation(self):
        total_amount = 200000
        wizard_riba_issue = self.env["presentation.riba.issue"].create(
            {"presentation_amount": total_amount}
        )
        domain = wizard_riba_issue.action_presentation_riba()["domain"]
        total_issue_amount = sum(
            self.env["account.move.line"].search(domain).mapped("amount_residual")
        )
        self.assertTrue(total_amount - total_issue_amount >= 0)

    def test_riba_bank_multicompany(self):
        """Configuration parameters for RiBa
        can only be created with data of current company."""
        current_company = self.env.company
        company_2 = self.company2
        partner_bank = self.company2_bank
        partner_bank.company_id = company_2
        suspense_account = self.bank_journal.suspense_account_id.copy(
            {"company_ids": [Command.link(company_2.id)]}
        )
        profit_account = self.bank_journal.profit_account_id.copy(
            {"company_ids": [Command.link(company_2.id)]}
        )
        loss_account = self.bank_journal.loss_account_id.copy(
            {"company_ids": [Command.link(company_2.id)]}
        )
        bank_journal = self.env["account.journal"].create(
            {
                "type": "bank",
                "name": "Bank Journal",
                "code": "BANK2",
                "company_id": company_2.id,
                "suspense_account_id": suspense_account.id,
                "profit_account_id": profit_account.id,
                "loss_account_id": loss_account.id,
            }
        )
        acceptance_account = self.acceptance_account.copy(
            {"company_ids": [Command.link(company_2.id)]}
        )
        # pre-condition
        self.assertEqual(partner_bank.company_id, company_2)
        self.assertNotEqual(current_company, company_2)

        # Act
        with self.assertRaises(UserError) as ue:
            self.env["riba.configuration"].create(
                {
                    "name": "Subject To Collection",
                    "type": "incasso",
                    "bank_id": partner_bank.id,
                    "acceptance_journal_id": bank_journal.id,
                    "acceptance_account_id": acceptance_account.id,
                }
            )

        # Assert
        exc_message = ue.exception.args[0]
        self.assertIn(current_company.name, exc_message)
        self.assertIn(partner_bank.display_name, exc_message)

    def test_riba_line_date_no_move(self):
        """
        The RiBa line can compute the date when the linked move has been deleted.
        """
        # Arrange: Create RiBa for an invoice
        self.invoice.company_id.due_cost_service_id = self.service_due_cost
        self.invoice.action_post()
        self.assertEqual(self.invoice.state, "posted")

        to_issue_action = self.env.ref("l10n_it_riba_oca.action_riba_to_issue")
        to_issue_model = self.env[to_issue_action.res_model]
        to_issue_domain = safe_eval.safe_eval(to_issue_action.domain)
        to_issue_records = (
            to_issue_model.search(to_issue_domain) & self.invoice.line_ids
        )
        self.assertTrue(to_issue_records)

        issue_wizard_context = {
            "active_model": to_issue_records._name,
            "active_ids": to_issue_records.ids,
        }
        issue_wizard_model = self.env["riba.issue"].with_context(**issue_wizard_context)
        issue_wizard_form = Form(issue_wizard_model)
        issue_wizard_form.configuration_id = self.riba_config_incasso
        issue_wizard = issue_wizard_form.save()
        issue_result = issue_wizard.create_list()

        # Act: Delete the invoice
        self.invoice.button_draft()
        self.invoice.unlink()

        # Assert: The dates on RiBa lines are empty
        riba_list_id = issue_result["res_id"]
        riba_list_model = issue_result["res_model"]
        riba_list = self.env[riba_list_model].browse(riba_list_id)
        self.assertEqual(
            riba_list.line_ids.mapped("invoice_date"),
            [False] * 2,
        )

    def test_file_substitute_forbidden_chars(self):
        """Forbidden characters are substituted in generated file."""
        # Arrange
        company = self.env.company
        company.vat = "IT00000000000"
        payment_term = self.payment_term1
        product = self.product1
        partner = self.partner
        partner.street = "Via di là"
        company.due_cost_service_id = self.service_due_cost

        invoice_form = Form(
            self.env["account.move"].with_context(
                default_move_type="out_invoice",
                default_name="Test invoice",
            )
        )
        invoice_form.partner_id = partner
        invoice_form.invoice_payment_term_id = payment_term
        invoice_form.riba_partner_bank_id = first(partner.bank_ids)
        with invoice_form.invoice_line_ids.new() as line:
            line.product_id = product
        invoice = invoice_form.save()
        invoice.action_post()

        to_issue_action = self.env.ref("l10n_it_riba_oca.action_riba_to_issue")
        to_issue_records = self.env[to_issue_action.res_model].search(
            safe_eval.safe_eval(to_issue_action.domain)
        )
        invoice_to_issue_records = to_issue_records & invoice.line_ids
        self.assertTrue(invoice_to_issue_records)

        issue_wizard_model = self.env["riba.issue"].with_context(
            active_model=invoice_to_issue_records._name,
            active_ids=invoice_to_issue_records.ids,
        )
        issue_wizard_form = Form(issue_wizard_model)
        issue_wizard_form.configuration_id = self.riba_config_incasso
        issue_wizard = issue_wizard_form.save()
        issue_result = issue_wizard.create_list()
        slip = self.env[issue_result["res_model"]].browse(issue_result["res_id"])

        # Act
        export_wizard = (
            self.env["riba.file.export"].with_context(active_ids=slip.ids).create({})
        )
        export_wizard.act_getfile()

        # Assert
        file_content = base64.decodebytes(export_wizard.riba_txt).decode()
        self.assertNotIn("Via di là", file_content)
        self.assertIn("Via di la", file_content)

    def test_riba_inv_no_bank(self):
        """
        Test that a riba invoice without a bank defined
        cannot be confirmed (e.g. via the list view)
        """
        self.invoice.company_id.due_cost_service_id = self.service_due_cost.id
        self.invoice.riba_partner_bank_id = False
        with self.assertRaises(UserError) as err:
            self.invoice.action_post()
        err_msg = err.exception.args[0]
        self.assertIn("Cannot post invoices", err_msg)
        self.assertIn(self.invoice.partner_id.display_name, err_msg)
        # We have to add back a taxed collection fee for each payment term line
        # because they have been added during `action_post`
        # and recorded in the exception message,
        # but `assertRaises` rolls them back
        collection_fees = self.invoice.invoice_payment_term_id.riba_payment_cost
        collection_fees_tax = self.invoice.fiscal_position_id.map_tax(
            self.service_due_cost.taxes_id
        )
        taxed_collection_fees = collection_fees_tax.compute_all(collection_fees)[
            "total_included"
        ]
        self.assertIn(
            str(
                self.invoice.amount_total
                + len(self.invoice.invoice_payment_term_id.line_ids)
                * taxed_collection_fees
            ),
            err_msg,
        )

    def test_riba_payment_date_multiple_lines(self):
        """A specific date can be set to pay multiple RiBa lines."""
        # Arrange
        company = self.env.company
        payment_date = datetime.date(2020, month=1, day=1)
        payment_term = self.payment_term2
        riba_configuration = self.riba_config_sbf
        product = self.product1
        partner = self.partner
        company.due_cost_service_id = self.service_due_cost

        invoice_form = Form(
            self.env["account.move"].with_context(
                default_move_type="out_invoice",
                default_name="Test invoice",
            )
        )
        invoice_form.partner_id = partner
        invoice_form.invoice_payment_term_id = payment_term
        invoice_form.riba_partner_bank_id = first(partner.bank_ids)
        with invoice_form.invoice_line_ids.new() as line:
            line.product_id = product
        invoice = invoice_form.save()
        invoice.action_post()

        to_issue_action = self.env.ref("l10n_it_riba_oca.action_riba_to_issue")
        to_issue_records = self.env[to_issue_action.res_model].search(
            safe_eval.safe_eval(to_issue_action.domain)
        )
        invoice_to_issue_records = to_issue_records & invoice.line_ids
        self.assertTrue(invoice_to_issue_records)

        issue_wizard_model = self.env["riba.issue"].with_context(
            active_model=invoice_to_issue_records._name,
            active_ids=invoice_to_issue_records.ids,
        )
        issue_wizard_form = Form(issue_wizard_model)
        issue_wizard_form.configuration_id = riba_configuration
        issue_wizard = issue_wizard_form.save()
        issue_result = issue_wizard.create_list()
        slip = self.env[issue_result["res_model"]].browse(issue_result["res_id"])

        slip.confirm()
        self.assertEqual(slip.state, "accepted")

        credit_wizard_action = self.env.ref("l10n_it_riba_oca.riba_credit_action")
        credit_wizard = (
            self.env[credit_wizard_action["res_model"]]
            .with_context(active_id=slip.id)
            .create(
                {
                    "credit_amount": invoice.amount_total,
                }
            )
        )
        res = credit_wizard.create_move()
        self.env["account.move"].browse([res["res_id"]]).action_post()
        self.assertEqual(slip.state, "credited")
        # Act
        payment_wizard_action = slip.settle_all_line()
        payment_wizard_form = Form(
            self.env[payment_wizard_action["res_model"]].with_context(
                **payment_wizard_action["context"]
            )
        )
        payment_wizard_form.payment_date = payment_date
        payment_wizard = payment_wizard_form.save()
        payment_wizard.pay()

        # Assert
        self.assertEqual(slip.state, "paid")
        payment_lines = self.env["account.move.line"].search(
            [("slip_line_id", "in", slip.line_ids.ids)]
        )
        self.assertTrue(payment_lines)
        payment_move = payment_lines[0].move_id
        self.assertEqual(payment_move.date, payment_date)

    def test_supplier_company_bank_account_domain(self):
        """The domain for Company Bank Account for Supplier
        only shows bank accounts of current company."""
        # Arrange
        current_company, other_company = self.env.company, self.company2
        current_bank_account = self.company_bank
        other_bank_account = self.company2_bank
        # pre-condition: Bank accounts belong to different companies
        self.assertNotEqual(current_company, other_company)
        self.assertEqual(current_bank_account.partner_id, current_company.partner_id)
        self.assertEqual(other_bank_account.partner_id, other_company.partner_id)

        # Act: Search bank accounts
        domain = self.env["res.partner"].fields_get(
            allfields=["property_riba_supplier_company_bank_id"],
            attributes=["domain"],
        )["property_riba_supplier_company_bank_id"]["domain"]
        bank_accounts = self.env["res.partner.bank"].search(domain)

        # Assert: only the bank account of current company is found
        self.assertIn(current_bank_account, bank_accounts)
        self.assertNotIn(other_bank_account, bank_accounts)

    def test_supplier_to_bill_company_bank_account(self):
        """A supplier has a company bank account,
        it is propagated to its vendor bill."""
        # Arrange
        bank_account = self.company_bank
        payment_term = self.payment_term1
        supplier = self.partner
        supplier.property_supplier_payment_term_id = payment_term
        supplier.property_riba_supplier_company_bank_id = bank_account
        self.assertTrue(payment_term.riba)

        # Act: Create the vendor bill
        bill = self.env["account.move"].create(
            {
                "move_type": "in_invoice",
                "partner_id": supplier.id,
                "invoice_payment_term_id": payment_term.id,
            }
        )

        # Assert
        self.assertEqual(bill.riba_supplier_company_bank_id, bank_account)

    def test_past_due_fee_amount_flow(self):
        config = self.env["riba.configuration"].create(
            {
                "name": "Test Config",
                "type": "sbf",
                "bank_id": self.company_bank.id,
                "acceptance_journal_id": self.bank_journal.id,
                "acceptance_account_id": self.acceptance_account.id,
                "past_due_fee_amount": 15.0,
            }
        )
        self.assertEqual(config.past_due_fee_amount, 15.0)
        distinta = self.env["riba.slip"].create(
            {
                "config_id": config.id,
                "name": "Test slip",
            }
        )
        distinta_line = self.env["riba.slip.line"].create(
            {"slip_id": distinta.id, "amount": 100.0}
        )
        wizard = (
            self.env["riba.past_due"]
            .with_context(
                active_model="riba.slip.line",
                active_id=distinta_line.id,
            )
            .create({})
        )
        self.assertEqual(wizard.past_due_fee_amount, 15.0)
