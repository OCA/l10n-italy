# Copyright 2018 Simone Rubino - Agile Business Group
# Copyright 2019 Alex Comba - Agile Business Group

import json

from odoo.exceptions import UserError
from odoo.tests import tagged

from .rc_common import ReverseChargeCommon


@tagged("post_install", "-at_install")
class TestReverseCharge(ReverseChargeCommon):
    def test_intra_EU_invoice_line_no_tax(self):
        invoice = self.create_invoice(self.supplier_intraEU, [], post=False)
        move_line_model = self.env["account.move.line"]
        move_line_model.create(
            {
                "account_id": self.invoice_line_account.id,
                "move_id": invoice.id,
                "price_unit": 100,
                "rc": True,
            }
        )
        with self.assertRaises(UserError):
            invoice.action_post()

    def test_intra_EU(self):
        self.supplier_intraEU.property_payment_term_id = self.term_15_30.id
        invoice = self.create_invoice(
            self.supplier_intraEU, amounts=[100], taxes=self.tax_22ai
        )

        self.assertIsNot(bool(invoice.rc_self_invoice_id), False)
        self.assertIsNot(bool(invoice.rc_self_invoice_id.invoice_payment_term_id), True)
        self.assertEqual(invoice.rc_self_invoice_id.state, "posted")
        self.assertEqual(invoice.rc_self_invoice_id.payment_id.move_id.state, "posted")
        self.assertTrue("Intra EU supplier" in invoice.rc_self_invoice_id.narration)

    def test_intra_EU_2_mixed_lines(self):
        """Create an invoice with two lines: one is RC and the other is not.
        By default, method `create_invoice` assigns the same RC flag to both
        lines, so we force one of them not to be RC"""
        invoice = self.create_invoice(
            self.supplier_intraEU, amounts=[100, 200], taxes=self.tax_22ai, post=False
        )
        invoice.invoice_line_ids[-1].rc = False
        invoice.action_post()

        # Only the tax in the RC line (22) should result as paid
        self.assertEqual(invoice.amount_total, 366.0)
        self.assertEqual(invoice.amount_residual, 344.0)

    def test_intra_EU_amount_tax_amount_payments_widget_discrepancy(self):
        """Create an invoice with round_globally where there was discrepancy
        between amount_tax (29.17) and amount shown on payments_widget (29.18).
        """
        inv_amounts = [43.35, 20.25, 20.60, 8, 28.25, 12, 0.13]
        invoice = self.create_invoice(
            self.supplier_intraEU, amounts=inv_amounts, taxes=self.tax_22ai
        )

        self.assertIsNot(bool(invoice.rc_self_invoice_id), False)
        self.assertIsNot(bool(invoice.rc_self_invoice_id.invoice_payment_term_id), True)
        self.assertEqual(invoice.rc_self_invoice_id.state, "posted")
        self.assertEqual(invoice.rc_self_invoice_id.payment_id.move_id.state, "posted")
        # compare amount_tax with amount show on paymenys_widget
        info = json.loads(invoice.invoice_payments_widget)["content"][0]
        self.assertEqual(info["amount"], invoice.amount_tax)

    def test_extra_EU(self):
        invoice = self.create_invoice(
            self.supplier_extraEU, amounts=[100], taxes=self.tax_22ai
        )

        self.assertIsNot(bool(invoice.rc_self_purchase_invoice_id), False)
        self.assertEqual(invoice.rc_self_purchase_invoice_id.state, "posted")
        self.assertEqual(
            invoice.rc_self_purchase_invoice_id.payment_id.move_id.state,
            "posted",
        )

        invoice.button_cancel()
        self.assertEqual(invoice.state, "cancel")
        invoice.button_draft()
        # see what done with "with invoice.env.do_in_draft()" in
        # button_draft
        invoice.refresh()
        self.assertEqual(invoice.state, "draft")

    def test_intra_EU_cancel_and_draft(self):
        invoice = self.create_invoice(self.supplier_intraEU, [100], taxes=self.tax_22ai)

        invoice.button_cancel()
        self.assertEqual(invoice.state, "cancel")
        invoice.button_draft()
        invoice.refresh()
        self.assertEqual(invoice.state, "draft")

    def test_intra_EU_zero_total(self):
        invoice = self.create_invoice(
            self.supplier_intraEU, [100, -100], taxes=self.tax_22ai
        )

        self.assertEqual(invoice.amount_total, 0)
        self.assertEqual(invoice.rc_self_invoice_id.amount_total, 0)
        self.assertEqual(invoice.state, "posted")
        self.assertEqual(invoice.rc_self_invoice_id.state, "posted")

        invoice.button_cancel()
        self.assertEqual(invoice.state, "cancel")
        self.assertFalse(invoice.rc_self_invoice_id)
        invoice.button_draft()
        invoice.refresh()
        self.assertEqual(invoice.state, "draft")

    def test_new_refund_flag(self):
        """Check that the lines of a new refund have the RC flag properly set."""
        invoice = self.create_invoice(
            self.supplier_extraEU, [100], taxes=self.tax_22ai, post=False
        )
        self.assertTrue(all(line.rc for line in invoice.invoice_line_ids))

    def test_intra_EU_exempt(self):
        invoice = self.create_invoice(
            self.supplier_intraEU_exempt, [100], taxes=self.tax_0_pur
        )

        self.assertEqual(invoice.amount_total, 100)
        self.assertEqual(invoice.amount_residual, 100)
        self.assertEqual(invoice.rc_self_invoice_id.state, "posted")
        self.assertEqual(invoice.rc_self_invoice_id.amount_total, 100)
        self.assertEqual(invoice.rc_self_invoice_id.amount_residual, 0)
        invoice.button_cancel()
        self.assertEqual(invoice.state, "cancel")
        invoice.button_draft()
        invoice.refresh()
        self.assertEqual(invoice.state, "draft")

    def test_intra_EU_draft_and_reconfirm(self):
        """Check that the payments are deleted if invoice is reset to draft."""
        self.supplier_intraEU.property_payment_term_id = self.term_15_30.id
        invoice = self.create_invoice(
            self.supplier_intraEU, amounts=[100], taxes=self.tax_22ai
        )

        inv_payment = invoice.payment_id
        rc_payment = invoice.rc_self_invoice_id.payment_id
        invoice.button_draft()

        self.assertEqual(invoice.rc_self_invoice_id.state, "draft")
        self.assertEqual(bool(invoice.payment_id), False)
        self.assertEqual(bool(invoice.rc_self_invoice_id.payment_id), False)

        invoice.action_post()
        self.assertEqual(invoice.rc_self_invoice_id.state, "posted")
        self.assertIsNot(invoice.payment_id, inv_payment)
        self.assertIsNot(invoice.rc_self_invoice_id.payment_id, rc_payment)
