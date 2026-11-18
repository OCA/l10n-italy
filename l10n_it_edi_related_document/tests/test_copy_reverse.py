import datetime

from lxml import etree

from odoo import Command
from odoo.tests import tagged

from odoo.addons.l10n_it_edi.tests.common import TestItEdi


@tagged("post_install_l10n", "post_install", "-at_install")
class TestRelatedDocumentCopyReverse(TestItEdi):
    """A copied or reversed move must not share the standard related document
    of the move it comes from."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Move = cls.env["account.move"].with_company(cls.company)
        cls.invoice = cls.Move.create(
            {
                "move_type": "out_invoice",
                "invoice_date": datetime.date(2022, 3, 24),
                "invoice_date_due": datetime.date(2022, 3, 24),
                "partner_id": cls.italian_partner_b.id,
                "partner_bank_id": cls.test_bank.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "line",
                            "quantity": 1,
                            "price_unit": 100.0,
                            "tax_ids": [
                                Command.set(cls.company_data_2["default_tax_sale"].ids)
                            ],
                        }
                    ),
                ],
                "l10n_it_origin_document_type": "purchase_order",
                "l10n_it_origin_document_name": "PO 001",
                "l10n_it_origin_document_date": datetime.date(2022, 3, 23),
                "l10n_it_cig": "CIG0000001",
                "l10n_it_cup": "CUP000000000001",
            }
        )
        cls.invoice.action_post()
        cls.invoice_document = cls.invoice.standard_related_document_id

    def _reverse(self, move):
        wizard = (
            self.env["account.move.reversal"]
            .with_context(active_model="account.move", active_ids=move.ids)
            .create(
                {
                    "date": datetime.date(2022, 3, 25),
                    "journal_id": move.journal_id.id,
                }
            )
        )
        action = wizard.reverse_moves()
        return self.env["account.move"].browse(action["res_id"])

    def _assert_invoice_document_intact(self):
        self.assertTrue(self.invoice_document.exists())
        self.assertEqual(
            self.invoice.standard_related_document_id, self.invoice_document
        )
        self.assertEqual(self.invoice.related_document_ids, self.invoice_document)
        self.assertEqual(self.invoice_document.invoice_id, self.invoice)
        self.assertRecordValues(
            self.invoice_document,
            [
                {
                    "type": "order",
                    "name": "PO 001",
                    "date": datetime.date(2022, 3, 23),
                    "cig": "CIG0000001",
                    "cup": "CUP000000000001",
                }
            ],
        )

    def _xml(self, move):
        return etree.fromstring(move._l10n_it_edi_render_xml())

    def test_setup(self):
        self.assertTrue(self.invoice_document)
        self._assert_invoice_document_intact()

    def test_reverse_does_not_share_standard_document(self):
        credit_note = self._reverse(self.invoice)
        self.assertFalse(credit_note.standard_related_document_id)
        self.assertFalse(credit_note.related_document_ids)
        self._assert_invoice_document_intact()

    def test_reverse_then_type_only_keeps_invoice_document(self):
        """Origin type without name on the credit note: the invoice keeps its row."""
        credit_note = self._reverse(self.invoice)
        credit_note.write({"l10n_it_origin_document_type": "purchase_order"})
        self.assertFalse(credit_note.related_document_ids)
        self._assert_invoice_document_intact()

    def test_reverse_then_clear_type_keeps_invoice_document(self):
        credit_note = self._reverse(self.invoice)
        credit_note.write({"l10n_it_origin_document_type": False})
        self._assert_invoice_document_intact()

    def test_reverse_then_full_standard_fields(self):
        """Full origin data on the credit note: it gets its own row."""
        credit_note = self._reverse(self.invoice)
        credit_note.write(
            {
                "l10n_it_origin_document_type": "purchase_order",
                "l10n_it_origin_document_name": "PO 002",
                "l10n_it_origin_document_date": datetime.date(2022, 3, 25),
                "l10n_it_cig": "CIG0000002",
            }
        )
        document = credit_note.standard_related_document_id
        self.assertTrue(document)
        self.assertEqual(document.invoice_id, credit_note)
        self.assertEqual(credit_note.related_document_ids, document)
        self.assertRecordValues(document, [{"name": "PO 002", "cig": "CIG0000002"}])
        self._assert_invoice_document_intact()

    def test_reverse_then_related_document_row(self):
        """A row added on the credit note becomes its standard document, fills
        the standard fields and passes the Public Administration check."""
        credit_note = self._reverse(self.invoice)
        credit_note.write(
            {
                "related_document_ids": [
                    Command.create(
                        {
                            "type": "order",
                            "name": "PO 001",
                            "date": datetime.date(2022, 3, 23),
                            "cig": "CIG0000001",
                        }
                    )
                ]
            }
        )
        document = credit_note.related_document_ids
        self.assertEqual(len(document), 1)
        self.assertEqual(credit_note.standard_related_document_id, document)
        self.assertRecordValues(
            credit_note,
            [
                {
                    "l10n_it_origin_document_type": "purchase_order",
                    "l10n_it_origin_document_name": "PO 001",
                    "l10n_it_cig": "CIG0000001",
                }
            ],
        )
        self.assertNotIn(
            "move_missing_origin_document",
            credit_note._l10n_it_edi_base_export_check(),
        )
        self._assert_invoice_document_intact()

        credit_note.action_post()
        tree = self._xml(credit_note)
        self.assertEqual(
            tree.xpath("//DatiOrdineAcquisto/IdDocumento/text()"), ["PO 001"]
        )
        self.assertEqual(
            tree.xpath("//DatiOrdineAcquisto/CodiceCIG/text()"), ["CIG0000001"]
        )
        self.assertEqual(
            tree.xpath("//DatiFattureCollegate/IdDocumento/text()"), [self.invoice.name]
        )

    def test_invoice_xml_after_reverse(self):
        credit_note = self._reverse(self.invoice)
        credit_note.write({"l10n_it_origin_document_type": "purchase_order"})
        tree = self._xml(self.invoice)
        self.assertEqual(
            tree.xpath("//DatiOrdineAcquisto/CodiceCIG/text()"), ["CIG0000001"]
        )
        self.assertEqual(
            tree.xpath("//DatiOrdineAcquisto/CodiceCUP/text()"), ["CUP000000000001"]
        )

    def test_copy_does_not_share_standard_document(self):
        copy = self.invoice.copy()
        self.assertFalse(copy.standard_related_document_id)
        self.assertFalse(copy.related_document_ids)
        self.assertFalse(copy.l10n_it_origin_document_type)
        copy.write({"l10n_it_origin_document_type": "purchase_order"})
        self._assert_invoice_document_intact()
        copy.write(
            {
                "l10n_it_origin_document_type": "purchase_order",
                "l10n_it_origin_document_name": "PO 003",
            }
        )
        self.assertEqual(copy.standard_related_document_id.invoice_id, copy)
        self.assertEqual(copy.standard_related_document_id.name, "PO 003")
        self._assert_invoice_document_intact()

    def test_reverse_and_create_new_draft(self):
        """'Reverse and create invoice' (modify) gives a new draft invoice that
        does not share the original row either."""
        wizard = (
            self.env["account.move.reversal"]
            .with_context(active_model="account.move", active_ids=self.invoice.ids)
            .create(
                {
                    "date": datetime.date(2022, 3, 25),
                    "journal_id": self.invoice.journal_id.id,
                }
            )
        )
        action = wizard.modify_moves()
        new_invoice = self.env["account.move"].browse(action["res_id"])
        self.assertEqual(new_invoice.move_type, "out_invoice")
        self.assertNotEqual(new_invoice, self.invoice)
        self.assertFalse(new_invoice.standard_related_document_id)
        new_invoice.write({"l10n_it_origin_document_type": False})
        self._assert_invoice_document_intact()
