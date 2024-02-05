# Author: Andrea Gallina
# ©  2015 Apulia Software srl
# Copyright (C) 2017 Lorenzo Battistini - Agile Business Group
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
import os

from odoo.tools import config

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

    def test_riba_flow(self):
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
                            "tax_ids": [[6, 0, []]],
                        },
                    )
                ],
            }
        )
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
            {"configuration_id": self.riba_config.id}
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
        self.assertEqual(len(riba_list.payment_ids), 0)

        # I print the RiBa slip report
        docargs = {
            "doc_ids": riba_list.ids,
            "doc_model": "riba.slip",
            "docs": self.env["riba.slip"].browse(riba_list.ids),
        }
        data = self.env["ir.qweb"]._render("l10n_it_riba.slip_qweb", docargs)
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
                    "bank_amount": 445,
                    "expense_amount": 5,
                }
            )
        )
        credit_wizard.create_move()
        self.assertEqual(riba_list.state, "credited")

        bank_credit_line = False
        for credit_line in riba_list.credit_move_id.line_ids:
            if credit_line.account_id.id == self.bank_account.id:
                bank_credit_line = credit_line
                break
        self.assertTrue(bank_credit_line)

        # register the bank statement with the bank credit
        # st = self.env['account.bank.statement'].create({
        #     'journal_id': self.bank_journal.id,
        #     'name': 'bank statement',
        #     'line_ids': [(0, 0, {
        #         'name': 'RiBa',
        #         'amount': 445,
        #     })]
        # })

        # must be possible to close the bank statement line with the
        # credit journal item generated by RiBa
        # move_lines_for_rec=st.line_ids[0].get_move_lines_for_reconciliation()
        # self.assertTrue(
        #     bank_credit_line.id in [l.id for l in move_lines_for_rec])
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
        riba_list.env.invalidate_all()
        self.assertEqual(riba_list.state, "paid")
        self.assertEqual(len(riba_list.payment_ids), 1)
        self.assertEqual(len(riba_list.line_ids), 1)
        self.assertEqual(riba_list.line_ids[0].state, "paid")
        to_reconcile.remove_move_reconcile()
        self.assertEqual(riba_list.state, "credited")
        self.assertEqual(riba_list.line_ids[0].state, "credited")

    def test_past_due_riba(self):
        # create another invoice to test past due RiBa
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
            {"configuration_id": self.riba_config.id}
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
                    "bank_amount": 95,
                    "expense_amount": 5,
                }
            )
        )

        credit_wizard.create_move()
        self.assertEqual(riba_list.state, "credited")

        # credit wizard with skip
        credit_wizard = (
            self.env["riba.credit"]
            .with_context(
                active_model="riba.slip",
                active_ids=[riba_list_id],
                active_id=riba_list_id,
            )
            .create(
                {
                    "bank_amount": 95,
                    "expense_amount": 5,
                }
            )
        )
        credit_wizard.skip()
        self.assertEqual(riba_list.state, "credited")
        self.assertEqual(riba_list.line_ids[0].state, "credited")

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
                    "bank_amount": 102,
                    "expense_amount": 2,
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
            if past_due_line.account_id.id == self.bank_account.id:
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

        riba_list.line_ids[0].past_due_move_id.line_ids.remove_move_reconcile()
        self.assertEqual(riba_list.state, "credited")
        self.assertEqual(len(riba_list.line_ids), 1)
        self.assertEqual(riba_list.line_ids[0].state, "credited")

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
            {"configuration_id": self.riba_config.id}
        )
        action = wizard_riba_issue.with_context(
            active_ids=[riba_move_line_id.id]
        ).create_list()
        riba_list_id = action and action["res_id"] or False
        riba_list = self.slip_model.browse(riba_list_id)
        riba_list.confirm()
        self.assertEqual(riba_list.line_ids[0].cig, "7987210EG5")
        self.assertEqual(riba_list.line_ids[0].cup, "H71N17000690124")
        wizard_riba_export = self.env["riba.file.export"].create({})
        wizard_riba_export.with_context(active_ids=[riba_list.id]).act_getfile()
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
                            "tax_ids": [[6, 0, self.tax_22.ids]],
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
                            "tax_ids": [[6, 0, self.tax_22.ids]],
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
            {"configuration_id": self.riba_config.id}
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
