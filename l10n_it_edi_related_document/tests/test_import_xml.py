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

    def test_standard_fields(self):
        euro = self.setup_other_currency("EUR")
        invoice = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.partner_a.id,
                "invoice_date": fields.Date.from_string("2016-01-01"),
                "currency_id": euro.id,
                "invoice_line_ids": [
                    (
                        0,
                        None,
                        {
                            "product_id": self.product_a.id,
                            "quantity": 3,
                            "price_unit": 750,
                        },
                    ),
                ],
            }
        )

        # add a document, via standard fields
        # note: this must be an atomic write(), as both name and type are required
        # fields and can't be assigned one a time
        invoice.write(
            {
                "l10n_it_origin_document_name": "S00001",
                "l10n_it_origin_document_type": "purchase_order",
                "l10n_it_origin_document_date": invoice.invoice_date,
                "l10n_it_cig": "CIG",
                "l10n_it_cup": "CUP",
            }
        )
        self.assertEqual(
            invoice.standard_related_document_id, invoice.related_document_ids[0]
        )
        self.assertEqual(invoice.standard_related_document_id.type, "order")
        self.assertEqual(invoice.standard_related_document_id.name, "S00001")
        self.assertEqual(
            invoice.standard_related_document_id.date, invoice.invoice_date
        )
        self.assertEqual(invoice.standard_related_document_id.cig, "CIG")
        self.assertEqual(invoice.standard_related_document_id.cup, "CUP")

        # alter the document
        invoice.standard_related_document_id.name = "S00002"
        invoice.standard_related_document_id.date = fields.Date.from_string(
            "2016-01-02"
        )
        invoice.standard_related_document_id.cig = "CIG2"
        invoice.standard_related_document_id.cup = "CUP2"

        # check if standard fields changed accordingly
        self.assertEqual(invoice.l10n_it_origin_document_name, "S00002")
        self.assertEqual(
            invoice.l10n_it_origin_document_date, fields.Date.from_string("2016-01-02")
        )
        self.assertEqual(invoice.l10n_it_cig, "CIG2")
        self.assertEqual(invoice.l10n_it_cup, "CUP2")
