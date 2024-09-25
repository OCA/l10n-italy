# Author: Andrea Gallina
# ©  2015 Apulia Software srl
# Copyright (C) 2017 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
import datetime
import os

from odoo.exceptions import UserError
from odoo.fields import first
from odoo.tests import Form
from odoo.tools import config, safe_eval

from . import riba_common


class TestInvoiceDueCost(riba_common.TestRibaCommon):
    def setUp(self):
        super(TestInvoiceDueCost, self).setUp()

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
        self.assertAlmostEqual(
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

    def riba_sbf_common(self, configuration_id):
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
                        ("unsolved_invoice_ids", "!=", False),
                        ("account_id.internal_type", "=", "receivable"),
                        ("reconciled", "=", False),
                        ("distinta_line_ids", "=", False),
                        ("move_id", "=", invoice.id),
                    ]
                )
                self.assertEqual(len(line_ids), 1)
                self.assertEqual(line_ids[0].id, move_line.id)
        self.assertTrue(riba_move_line_id)

        # issue wizard
        wizard_riba_issue = self.env["riba.issue"].create(
            {"configuration_id": configuration_id}
        )
        action = wizard_riba_issue.with_context(
            {"active_ids": [riba_move_line_id]}
        ).create_list()
        riba_list_id = action and action["res_id"] or False
        riba_list = self.distinta_model.browse(riba_list_id)
        riba_list.confirm()
        self.assertEqual(riba_list.state, "accepted")
        self.assertEqual(invoice.state, "posted")

        # Se la compute non viene invocata il test fallisce
        riba_list._compute_acceptance_move_ids()
        self.assertEqual(len(riba_list.acceptance_move_ids), 1)
        self.assertEqual(len(riba_list.payment_ids), 0)

        # I print the C/O distinta report
        docargs = {
            "doc_ids": riba_list.ids,
            "doc_model": "riba.distinta",
            "docs": self.env["riba.distinta"].browse(riba_list.ids),
        }
        data = self.env.ref("l10n_it_ricevute_bancarie.distinta_qweb")._render(docargs)
        if config.get("test_report_directory"):
            open(
                os.path.join(config["test_report_directory"], "riba-list." + format),
                "wb+",
            ).write(data)

        # credit wizard
        wiz_accreditation = (
            self.env["riba.accreditation"]
            .with_context(
                {
                    "active_model": "riba.distinta",
                    "active_ids": [riba_list_id],
                    "active_id": riba_list_id,
                }
            )
            .create(
                {
                    "bank_amount": 445,
                    "expense_amount": 5,
                }
            )
        )
        wiz_accreditation.create_move()
        self.assertEqual(riba_list.state, "accredited")
        return invoice, riba_list

    def test_riba_sbf_maturation_flow(self):
        invoice, riba_list = self.riba_sbf_common(self.riba_config_sbf_maturation.id)

        bank_accreditation_line = False
        for accr_line in riba_list.accreditation_move_id.line_ids:
            if accr_line.account_id.id == self.bank_account.id:
                bank_accreditation_line = accr_line
                break
        self.assertTrue(bank_accreditation_line)

        # register the bank statement with the bank credit
        # st = self.env['account.bank.statement'].create({
        #     'journal_id': self.bank_journal.id,
        #     'name': 'bank statement',
        #     'line_ids': [(0, 0, {
        #         'name': 'C/O',
        #         'amount': 445,
        #     })]
        # })

        # must be possible to close the bank statement line with the
        # credit journal item generated by C/O
        # move_lines_for_rec=st.line_ids[0].get_move_lines_for_reconciliation()
        # self.assertTrue(
        #     bank_accreditation_line.id in [l.id for l in move_lines_for_rec])
        #
        # bank notifies cash in
        bank_move = self.move_model.create(
            {
                "journal_id": self.bank_journal.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "partner_id": self.partner.id,
                            "account_id": self.sbf_effects.id,
                            "credit": 450,
                            "debit": 0,
                            "name": "sbf effects",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "partner_id": self.partner.id,
                            "account_id": self.riba_account.id,
                            "credit": 0,
                            "debit": 450,
                            "name": "Banca conto ricevute bancarie",
                        },
                    ),
                ],
            }
        )
        bank_move.action_post()
        to_reconcile = self.env["account.move.line"]
        line_set = bank_move.line_ids | riba_list.acceptance_move_ids[0].line_ids
        for line in line_set:
            if line.account_id.id == self.sbf_effects.id:
                to_reconcile |= line
        self.assertEqual(len(to_reconcile), 2)
        to_reconcile.reconcile()
        # refresh otherwise riba_list.payment_ids is not recomputed
        riba_list.refresh()
        self.assertEqual(riba_list.state, "paid")
        self.assertEqual(len(riba_list.payment_ids), 1)
        self.assertEqual(len(riba_list.line_ids), 1)
        self.assertEqual(riba_list.line_ids[0].state, "paid")
        to_reconcile.remove_move_reconcile()
        self.assertEqual(riba_list.state, "accredited")
        self.assertEqual(riba_list.line_ids[0].state, "accredited")

    def test_riba_sbf_immediate_flow(self):
        invoice, riba_list = self.riba_sbf_common(self.riba_config_sbf_immediate.id)

        # past due wizard
        unsolved_wizard = (
            self.env["riba.unsolved"]
            .with_context(
                active_model="riba.distinta.line",
                active_ids=[riba_list.line_ids[0].id],
                active_id=riba_list.line_ids[0].id,
            )
            .create(
                {
                    "bank_amount": 455,
                    "expense_amount": 5,
                }
            )
        )
        unsolved_wizard.create_move()
        self.assertEqual(riba_list.state, "unsolved")
        self.assertEqual(len(riba_list.line_ids), 1)
        self.assertEqual(riba_list.line_ids[0].state, "unsolved")
        self.assertTrue(invoice.unsolved_move_line_ids)

        # Verifica storno registrazioni di presentazione della RiBa
        unsolved_line_ids = riba_list.line_ids.unsolved_move_id.line_ids
        unsolved_line_id_bills = unsolved_line_ids.filtered(
            lambda line: line.name == "Bills"
        )
        self.assertEqual(len(unsolved_line_id_bills), 1)
        self.assertEqual(
            unsolved_line_id_bills.account_id, unsolved_wizard.effects_account_id
        )
        self.assertEqual(unsolved_line_id_bills.credit, unsolved_wizard.effects_amount)
        unsolved_line_id_riba = unsolved_line_ids.filtered(
            lambda line: line.name == "C/O"
        )
        self.assertEqual(len(unsolved_line_id_riba), 1)
        self.assertEqual(
            unsolved_line_id_riba.account_id, unsolved_wizard.riba_bank_account_id
        )
        self.assertEqual(unsolved_line_id_riba.debit, unsolved_wizard.riba_bank_amount)

        # Se la compute non viene invocata il test fallisce
        riba_list._compute_unsolved_move_ids()
        self.assertEqual(len(riba_list.unsolved_move_ids), 1)
        bank_unsolved_line = False
        for unsolved_line in riba_list.unsolved_move_ids[0].line_ids:
            if unsolved_line.account_id.id == self.bank_account.id:
                bank_unsolved_line = unsolved_line
                break
        self.assertTrue(bank_unsolved_line)

    def test_riba_incasso_flow(self):
        """
        RiBa of type 'After Collection' pays invoice when accepted.
        """
        self.invoice.company_id.due_cost_service_id = self.service_due_cost
        self.invoice.action_post()
        self.assertEqual(self.invoice.state, "posted")

        to_issue_action = self.env.ref(
            "l10n_it_ricevute_bancarie.action_riba_da_emettere"
        )
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
        self.assertEqual(self.invoice.payment_state, "paid")

    def test_unsolved_riba(self):
        # create another invoice to test past due C/O
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
            {"configuration_id": self.riba_config_sbf_maturation.id}
        )
        action = wizard_riba_issue.with_context(
            {"active_ids": [riba_move_line_id]}
        ).create_list()
        riba_list_id = action and action["res_id"] or False
        riba_list = self.distinta_model.browse(riba_list_id)
        riba_list.confirm()
        self.assertEqual(riba_list.state, "accepted")
        self.assertEqual(invoice.state, "posted")
        # credit wizard
        wiz_accreditation = (
            self.env["riba.accreditation"]
            .with_context(
                {
                    "active_model": "riba.distinta",
                    "active_ids": [riba_list_id],
                    "active_id": riba_list_id,
                }
            )
            .create(
                {
                    "bank_amount": 95,
                    "expense_amount": 5,
                }
            )
        )
        wiz_accreditation.create_move()
        self.assertEqual(riba_list.state, "accredited")

        # credit wizard with skip
        credit_wizard = (
            self.env["riba.accreditation"]
            .with_context(
                {
                    "active_model": "riba.distinta",
                    "active_ids": [riba_list_id],
                    "active_id": riba_list_id,
                }
            )
            .create(
                {
                    "bank_amount": 95,
                    "expense_amount": 5,
                }
            )
        )
        credit_wizard.skip()
        self.assertEqual(riba_list.state, "accredited")

        self.assertEqual(riba_list.line_ids[0].state, "accredited")

        # past due wizard
        wiz_unsolved = (
            self.env["riba.unsolved"]
            .with_context(
                {
                    "active_model": "riba.distinta.line",
                    "active_ids": [riba_list.line_ids[0].id],
                    "active_id": riba_list.line_ids[0].id,
                }
            )
            .create(
                {
                    "bank_amount": 102,
                    "expense_amount": 2,
                }
            )
        )
        wiz_unsolved.create_move()
        self.assertEqual(riba_list.state, "unsolved")
        self.assertEqual(len(riba_list.line_ids), 1)
        self.assertEqual(riba_list.line_ids[0].state, "unsolved")
        self.assertTrue(invoice.unsolved_move_line_ids)

        # Se la compute non viene invocata il test fallisce
        riba_list._compute_unsolved_move_ids()
        self.assertEqual(len(riba_list.unsolved_move_ids), 1)
        bank_unsolved_line = False
        for unsolved_line in riba_list.unsolved_move_ids[0].line_ids:
            if unsolved_line.account_id.id == self.bank_account.id:
                bank_unsolved_line = unsolved_line
                break
        self.assertTrue(bank_unsolved_line)

        # register the bank statement with the bank credit
        # st = self.env['account.bank.statement'].create({
        #     'journal_id': self.bank_journal.id,
        #     'name': 'bank statement',
        #     'line_ids': [(0, 0, {
        #         'name': 'C/O',
        #         'amount': -102,
        #     })]
        # })
        # must be possible to close the bank statement line with the
        # past due journal item generated by C/O
        # move_lines_for_rec=st.line_ids[0].get_move_lines_for_reconciliation()
        # self.assertTrue(
        #     bank_unsolved_line.id in [l.id for l in move_lines_for_rec])

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
                        },
                    )
                ],
                "related_documents": [
                    (
                        0,
                        0,
                        {
                            "type": "order",
                            "name": "SO1232",
                            "cig": "7987210EG5",
                            "cup": "H71N17000690124",
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
            {"configuration_id": self.riba_config_sbf_maturation.id}
        )
        action = wizard_riba_issue.with_context(
            {"active_ids": [riba_move_line_id.id]}
        ).create_list()
        riba_list_id = action and action["res_id"] or False
        riba_list = self.distinta_model.browse(riba_list_id)
        riba_list.confirm()
        self.assertEqual(riba_list.line_ids[0].cig, "7987210EG5")
        self.assertEqual(riba_list.line_ids[0].cup, "H71N17000690124")
        wizard_riba_export = self.env["riba.file.export"].create({})
        wizard_riba_export.with_context({"active_ids": [riba_list.id]}).act_getfile()
        riba_txt = base64.decodebytes(wizard_riba_export.riba_txt)
        self.assertTrue(b"CIG: 7987210EG5 CUP: H71N17000690124" in riba_txt)

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
                        },
                    )
                ],
                "related_documents": [
                    (
                        0,
                        0,
                        {
                            "type": "order",
                            "name": "SO1232",
                            "cig": "7987210EG5",
                            "cup": "H71N17000690124",
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
                        },
                    )
                ],
                "related_documents": [
                    (
                        0,
                        0,
                        {
                            "type": "order",
                            "name": "SO1232",
                            "cig": "7987210EG5",
                            "cup": "H71N17000690125",
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
            {"configuration_id": self.riba_config_sbf_maturation.id}
        )
        action = wizard_riba_issue.with_context(
            {"active_ids": [riba_move_line_id.id, riba_move_line1_id.id]}
        ).create_list()
        riba_list_id = action and action["res_id"] or False
        riba_list = self.distinta_model.browse(riba_list_id)
        riba_list.confirm()
        self.assertTrue(len(riba_list.line_ids), 2)
        wizard_riba_export = self.env["riba.file.export"].create({})
        wizard_riba_export.with_context({"active_ids": [riba_list.id]}).act_getfile()
        riba_txt = base64.decodebytes(wizard_riba_export.riba_txt)
        self.assertTrue(b"CIG: 7987210EG5 CUP: H71N17000690124" in riba_txt)
        self.assertTrue(b"CIG: 7987210EG5 CUP: H71N17000690125" in riba_txt)

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
        with self.assertRaises(UserError) as ue:
            self.env["riba.configuration"].create(
                {
                    "name": "Subject To Collection",
                    "type": "incasso",
                    "bank_id": self.company2_bank.id,
                }
            )
        exc_message = ue.exception.args[0]
        self.assertIn(self.env.company.name, exc_message)
        self.assertIn(self.company2_bank.acc_number, exc_message)

    def test_riba_line_date_no_move(self):
        """
        The RiBa line can compute the date when the linked move has been deleted.
        """
        # Arrange: Create RiBa for an invoice
        self.invoice.company_id.due_cost_service_id = self.service_due_cost
        self.invoice.action_post()
        self.assertEqual(self.invoice.state, "posted")

        to_issue_action = self.env.ref(
            "l10n_it_ricevute_bancarie.action_riba_da_emettere"
        )
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
        self.invoice.with_context(force_delete=True).unlink()

        # Assert: The dates on RiBa lines are empty
        riba_list_id = issue_result["res_id"]
        riba_list_model = issue_result["res_model"]
        riba_list = self.env[riba_list_model].browse(riba_list_id)
        self.assertEqual(
            riba_list.line_ids.mapped("invoice_date"),
            [False] * 2,
        )

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
        self.assertIn(str(self.invoice.amount_total), err_msg)

    def test_riba_payment_date_multiple_lines(self):
        """A specific date can be set to pay multiple RiBa lines."""
        # Arrange
        company = self.env.company
        payment_date = datetime.date(2020, month=1, day=1)
        payment_term = self.payment_term2
        riba_configuration = self.riba_config_sbf_immediate
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

        to_issue_action = self.env.ref(
            "l10n_it_ricevute_bancarie.action_riba_da_emettere"
        )
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

        credit_wizard_action = self.env.ref(
            "l10n_it_ricevute_bancarie.riba_accreditation_action"
        )
        credit_wizard = (
            self.env[credit_wizard_action["res_model"]]
            .with_context(active_id=slip.id)
            .create(
                {
                    "bank_amount": invoice.amount_total,
                }
            )
        )
        credit_wizard.create_move()
        self.assertEqual(slip.state, "accredited")

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
        payment_move = slip.payment_ids.move_id
        self.assertEqual(payment_move.date, payment_date)
