from odoo import fields

from odoo.addons.l10n_it_edi.tests.common import TestItEdi


class TestItEdiImport(TestItEdi):
    """Main test class for the l10n_it_edi vendor bills XML import"""

    def test_receive_vendor_bill(self):
        """Test a sample e-invoice file with multiple related documents"""
        self.module = "l10n_it_edi_related_document"
        invoice = self._assert_import_invoice(
            "IT01234567888_FPR01_02.xml",
            [
                {
                    "move_type": "in_invoice",
                    "invoice_date": fields.Date.from_string("2014-12-18"),
                    "amount_untaxed": 39.0,
                    "amount_tax": 6.38,
                }
            ],
        )
        related_document = invoice.related_document_ids
        self.assertEqual(len(related_document), 2)
        invoice_doc_type = related_document.filtered(lambda x: x.type == "invoice")[0]
        rcp_doc_type = related_document.filtered(lambda x: x.type == "reception")[0]
        self.assertTrue(invoice_doc_type)
        self.assertTrue(rcp_doc_type)
        self.assertEqual(invoice_doc_type.cig, "5554466")
        self.assertEqual(rcp_doc_type.cup, "5678")
        self.assertTrue(
            invoice.line_ids.filtered(lambda x: rcp_doc_type in x.related_document_ids)
        )
