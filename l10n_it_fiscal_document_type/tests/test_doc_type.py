# Copyright 2017 Lorenzo Battistini
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tests import Form, tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.addons.l10n_it_account.tools.account_tools import fpa_schema_get_enum


@tagged("post_install", "-at_install")
class TestDocType(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.journalrec = cls.company_data["default_journal_misc"]

        cls.doc_type_model = cls.env["fiscal.document.type"]
        cls.TD01 = cls.doc_type_model.search([("code", "=", "TD01")], limit=1)
        cls.TD10 = cls.doc_type_model.search([("code", "=", "TD10")], limit=1)
        cls.TD01.journal_ids = cls.journalrec
        cls.TD04 = cls.doc_type_model.search([("code", "=", "TD04")], limit=1)
        cls.inv_model = cls.env["account.move"]
        cls.partner3 = cls.env.ref("base.res_partner_3")
        cls.partner4 = cls.env.ref("base.res_partner_4")
        cls.fp = cls.env["account.fiscal.position"].create(
            {
                "name": "FP",
                "fiscal_document_type_id": cls.TD01.id,
            }
        )
        cls.fp_td10 = cls.env["account.fiscal.position"].create(
            {
                "name": "FP",
                "fiscal_document_type_id": cls.TD10.id,
            }
        )
        cls.partner4.property_account_position_id = cls.fp_td10

    def test_doc_type(self):
        invoice = self.inv_model.with_context(default_move_type="out_invoice").create(
            {"partner_id": self.partner3.id}
        )
        self.assertEqual(invoice.move_type, "out_invoice")
        self.assertEqual(invoice.fiscal_document_type_id.id, self.TD01.id)

        invoice2 = self.inv_model.with_context(default_move_type="in_invoice").create(
            {"partner_id": self.partner3.id}
        )
        self.assertEqual(invoice2.move_type, "in_invoice")
        self.assertEqual(invoice2.fiscal_document_type_id.id, self.TD01.id)

    def test_doc_type_on_invoice_create(self):
        """Check document type on invoice create based invoice type."""
        product = self.env.ref("product.product_product_5")
        # Create a standard vendor invoice
        invoice = self.init_invoice(
            "in_invoice", partner=self.partner3, products=product
        )
        self.assertEqual(invoice.move_type, "in_invoice")
        self.assertEqual(invoice.fiscal_document_type_id, self.TD01)
        # Create a standard customer refund
        invoice = self.init_invoice(
            "out_refund", partner=self.partner3, products=product
        )
        self.assertEqual(invoice.move_type, "out_refund")
        self.assertEqual(invoice.fiscal_document_type_id, self.TD04)
        # Create a customer invoice for a partner with a fiscal position with TD10,
        # which is not applicable for "out_invoice" so it's applied the default TD01
        invoice = self.init_invoice(
            "out_invoice", partner=self.partner4, products=product
        )
        self.assertEqual(invoice.move_type, "out_invoice")
        self.assertEqual(invoice.fiscal_document_type_id, self.TD01)
        # Create a vendor invoice for a partner with a fiscal position with TD10,
        # which is applied as applicable for "in_invoice".
        invoice = self.init_invoice(
            "in_invoice", partner=self.partner4, products=product
        )
        self.assertEqual(invoice.move_type, "in_invoice")
        self.assertEqual(invoice.fiscal_document_type_id, self.TD10)
        # Create a standard customer invoice and a linked refund
        invoice = self.init_invoice(
            "out_invoice", partner=self.partner3, products=product, post=True
        )
        self.assertEqual(invoice.move_type, "out_invoice")
        self.assertEqual(invoice.fiscal_document_type_id, self.TD01)

        move_reversal = (
            self.env["account.move.reversal"]
            .with_context(active_model="account.move", active_ids=invoice.ids)
            .create(
                {
                    "reason": "no reason",
                    "refund_method": "cancel",
                }
            )
        )
        reversal = move_reversal.reverse_moves()
        reverse_move = self.env["account.move"].browse(reversal["res_id"])
        self.assertEqual(reverse_move.move_type, "out_refund")
        self.assertEqual(reverse_move.fiscal_document_type_id.id, self.TD04.id)

    def _set_recompute_document_type(self, invoice, doc_type):
        """Set a document type and recompute the field."""
        # Set document type
        invoice_form = Form(invoice)
        invoice_form.fiscal_document_type_id = doc_type
        invoice = invoice_form.save()
        self.assertEqual(invoice.fiscal_document_type_id, doc_type)

        # Recompute document type for the invoice
        self.env.add_to_compute(invoice._fields["fiscal_document_type_id"], invoice)
        self.inv_model.flush()
        return invoice

    def test_keep_edited_invoice(self):
        """Check that the changes performed by the user
        are kept through a recomputation if acceptable."""
        invoice = self.init_invoice("out_invoice", products=self.product_a)
        self.assertTrue(invoice.fiscal_document_type_id)

        # Change document type to a not accepted TD04 and check it gets changed
        td04 = self.TD04
        invoice = self._set_recompute_document_type(invoice, td04)
        self.assertNotEqual(invoice.fiscal_document_type_id, td04)

        # Change document type to an accepted TD02 and check it is kept
        td02 = self.doc_type_model.search([("code", "=", "TD02")], limit=1)
        invoice = self._set_recompute_document_type(invoice, td02)
        self.assertEqual(invoice.fiscal_document_type_id, td02)

    def test_compare_with_fpa_schema(self):
        """Check that the values we define in this module are
        the same as those defined in FPA xsd"""

        my_codes = self.doc_type_model.search([]).mapped("code")

        # XXX hardcoded: fattura elettronica semplificata
        my_codes = [code for code in my_codes if code not in ["TD07", "TD08", "TD09"]]

        # XXX hardcoded: esterometro
        my_codes = [code for code in my_codes if code not in ["TD10", "TD11", "TD12"]]

        # from fatturapa xml Schema
        xsd_codes = [code for code, descr in fpa_schema_get_enum("TipoDocumentoType")]

        self.assertCountEqual(my_codes, xsd_codes)
