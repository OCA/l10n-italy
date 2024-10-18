# Copyright 2024 Giuseppe Borruso - Dinamiche Aziendali srl

from odoo.tests import tagged

from odoo.addons.l10n_it_reverse_charge.tests.test_rc import TestReverseCharge


@tagged("post_install", "-at_install")
class TestReverseChargeTripleDiscount(TestReverseCharge):
    def test_intra_EU(self):
        self.supplier_intraEU.property_payment_term_id = self.term_15_30.id
        invoice = self.create_invoice(
            self.supplier_intraEU, amounts=[100], taxes=self.tax_22ai, post=False
        )
        invoice.invoice_line_ids[-1].discount = 20.0
        invoice.invoice_line_ids[-1].discount2 = 10.0
        invoice.action_post()

        self.assertIsNot(bool(invoice.rc_self_invoice_id), False)
        self.assertEqual(invoice.rc_self_invoice_id.state, "posted")
        self.assertEqual(
            invoice.rc_self_invoice_id.amount_untaxed, invoice.amount_untaxed
        )

    def test_extra_EU(self):
        invoice = self.create_invoice(
            self.supplier_extraEU, amounts=[100], taxes=self.tax_0_pur, post=False
        )
        invoice.invoice_line_ids[-1].discount = 20.0
        invoice.invoice_line_ids[-1].discount2 = 10.0
        invoice.action_post()

        self.assertIsNot(bool(invoice.rc_self_purchase_invoice_id), False)
        self.assertEqual(invoice.rc_self_purchase_invoice_id.state, "posted")
        self.assertEqual(
            invoice.rc_self_purchase_invoice_id.amount_untaxed, invoice.amount_untaxed
        )
