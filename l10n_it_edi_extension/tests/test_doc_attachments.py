# Copyright 2026 Luca Orioli <lucaorioli@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from lxml import etree

from odoo import Command, tools
from odoo.exceptions import UserError
from odoo.modules.module import load_script
from odoo.tests import tagged

from odoo.addons.l10n_it_edi.tests.common import TestItEdi

from ..models.account_move import DOC_ATTACHMENT_FIELD


@tagged("post_install_l10n", "post_install", "-at_install")
class TestDocAttachments(TestItEdi):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.attachment = cls.env["ir.attachment"].create(
            {
                "name": "contract.pdf",
                "raw": b"%PDF-1.4 test",
            }
        )

    def _create_invoice(self, attachments=None, post=True):
        invoice = self.init_invoice(
            "out_invoice",
            amounts=[100],
            company=self.company,
            partner=self.italian_partner_a,
            taxes=self.default_tax,
        )
        invoice.invoice_date_due = invoice.date
        if attachments:
            invoice.l10n_it_edi_ext_doc_attachment_ids = [Command.set(attachments.ids)]
        if post:
            invoice.action_post()
        return invoice

    def _get_xml_attachment_nodes(self, invoice):
        tree = etree.fromstring(invoice._l10n_it_edi_render_xml())
        return tree.findall(".//Allegati")

    def test_export_doc_attachment(self):
        """Each e-invoice attachment is exported in an Allegati node."""
        invoice = self._create_invoice(self.attachment)
        nodes = self._get_xml_attachment_nodes(invoice)
        self.assertEqual(len(nodes), 1)
        node = nodes[0]
        self.assertEqual(node.findtext("NomeAttachment"), "contract.pdf")
        self.assertEqual(node.findtext("FormatoAttachment"), "PDF")
        # Without a description, the file name without extension
        self.assertEqual(node.findtext("DescrizioneAttachment"), "contract")
        self.assertEqual(
            base64.b64decode(node.findtext("Attachment")), b"%PDF-1.4 test"
        )

    def test_export_doc_attachment_description(self):
        """The description of a file of the invoice is exported."""
        self.attachment.description = "Signed\n  contract"
        invoice = self._create_invoice(self.attachment)
        node = self._get_xml_attachment_nodes(invoice)[0]
        self.assertEqual(node.findtext("DescrizioneAttachment"), "Signed contract")

    def test_export_shared_attachment_description_ignored(self):
        """The description of a file of another record is not exported."""
        partner_file = self.env["ir.attachment"].create(
            {
                "name": "shared.pdf",
                "raw": b"%PDF-1.4 shared",
                "res_model": "res.partner",
                "res_id": self.italian_partner_a.id,
                "description": "Internal note",
            }
        )
        invoice = self._create_invoice(partner_file)
        node = self._get_xml_attachment_nodes(invoice)[0]
        self.assertEqual(node.findtext("DescrizioneAttachment"), "shared")

    def test_export_without_doc_attachments(self):
        """Without e-invoice attachments, the XML is unchanged."""
        invoice = self._create_invoice()
        self.assertFalse(self._get_xml_attachment_nodes(invoice))

    def test_attachment_name_keeps_extension(self):
        """Long names are truncated to 60 characters keeping the extension."""
        name = self.env["account.move"]._l10n_it_edi_ext_attachment_xml_name(
            "a" * 80 + ".pdf"
        )
        self.assertEqual(len(name), 60)
        self.assertTrue(name.endswith(".pdf"))

    def test_estimated_xml_size_not_below_actual(self):
        """The estimated XML size is not below the size of the rendered XML."""
        invoice = self._create_invoice(self.attachment)
        self.assertGreaterEqual(
            invoice._l10n_it_edi_ext_estimated_xml_size(),
            len(invoice._l10n_it_edi_render_xml()),
        )

    def test_estimated_xml_size_includes_invoice_pdf(self):
        """The invoice PDF, if already generated, is counted in the estimate."""
        invoice = self._create_invoice(self.attachment)
        size = invoice._l10n_it_edi_ext_estimated_xml_size()
        invoice.invoice_pdf_report_file = base64.b64encode(b"%PDF-1.4" + b"0" * 2992)
        self.assertEqual(invoice._l10n_it_edi_ext_estimated_xml_size(), size + 4000)

    def test_export_check_size_margin(self):
        """The XML is rejected 100 KB before the SdI limit of 5 MB."""
        # 3,860,000 bytes are 5,146,667 once encoded: below 5 MB (5,242,880)
        # but above 5 MB less the 100 KB margin (5,140,480)
        big_attachment = self.env["ir.attachment"].create(
            {"name": "big.pdf", "raw": b"%PDF-1.4" + b"0" * 3_859_992}
        )
        invoice = self._create_invoice(big_attachment, post=False)
        self.assertIn(
            "l10n_it_edi_ext_doc_attachments_too_big",
            invoice._l10n_it_edi_export_data_check(),
        )
        invoice.l10n_it_edi_ext_doc_attachment_ids = [Command.set(self.attachment.ids)]
        self.assertNotIn(
            "l10n_it_edi_ext_doc_attachments_too_big",
            invoice._l10n_it_edi_export_data_check(),
        )

    def test_orphan_attachment_linked_to_move(self):
        """Attachments uploaded before saving are linked to the move field."""
        self.assertFalse(self.attachment.res_id)
        invoice = self._create_invoice(self.attachment)
        self.assertEqual(self.attachment.res_model, "account.move")
        self.assertEqual(self.attachment.res_id, invoice.id)
        self.assertEqual(self.attachment.res_field, DOC_ATTACHMENT_FIELD)
        # Still visible in the field, despite res_field
        invoice.invalidate_recordset()
        self.assertEqual(invoice.l10n_it_edi_ext_doc_attachment_ids, self.attachment)

    def test_chatter_shows_listed_attachments(self):
        """The chatter (and its preview) shows the listed attachments of the move."""
        invoice = self._create_invoice(self.attachment)
        self.assertIn(self.attachment, invoice._get_mail_thread_data_attachments())

    def test_removed_attachment_deleted(self):
        """A file of the move removed from the list is deleted."""
        invoice = self._create_invoice(self.attachment)
        invoice.message_main_attachment_id = self.attachment
        invoice.l10n_it_edi_ext_doc_attachment_ids = [
            Command.unlink(self.attachment.id)
        ]
        self.assertFalse(self.attachment.exists())
        self.assertFalse(invoice.message_main_attachment_id)

    def test_shared_attachment_kept(self):
        """A file of another record is kept, and shown only where it is listed."""
        partner_file = self.env["ir.attachment"].create(
            {
                "name": "shared.pdf",
                "raw": b"%PDF-1.4 shared",
                "res_model": "res.partner",
                "res_id": self.italian_partner_a.id,
            }
        )
        invoice_1 = self._create_invoice(partner_file)
        invoice_2 = self._create_invoice(partner_file)
        invoice_1.l10n_it_edi_ext_doc_attachment_ids = [Command.unlink(partner_file.id)]
        self.assertTrue(partner_file.exists())
        self.assertEqual(partner_file.res_model, "res.partner")
        self.assertNotIn(partner_file, invoice_1._get_mail_thread_data_attachments())
        self.assertIn(partner_file, invoice_2._get_mail_thread_data_attachments())

    def test_unlink_listed_attachment_forbidden(self):
        """A file listed in the e-invoice attachments cannot be deleted."""
        self._create_invoice(self.attachment)
        with self.assertRaises(UserError):
            self.attachment.unlink()

    def _generate_xml(self, invoice, pdf_values=None):
        xml = invoice._l10n_it_edi_render_xml(pdf_values=pdf_values)
        invoice.l10n_it_edi_attachment_file = base64.b64encode(xml)

    def test_xml_attachments_missing(self):
        """The XML is flagged when an attachment of the list is missing."""
        invoice = self._create_invoice()
        self._generate_xml(invoice)
        self.assertTrue(invoice.l10n_it_edi_ext_xml_generated)
        self.assertFalse(invoice.l10n_it_edi_ext_xml_attachments_missing)

        invoice.l10n_it_edi_ext_doc_attachment_ids = [Command.link(self.attachment.id)]
        self.assertTrue(invoice.l10n_it_edi_ext_xml_attachments_missing)
        self.assertFalse(invoice.l10n_it_edi_ext_xml_attachments_removed)

        self._generate_xml(invoice)
        self.assertFalse(invoice.l10n_it_edi_ext_xml_attachments_missing)
        self.assertEqual(
            [att["name"] for att in invoice.l10n_it_edi_ext_xml_attachments_data],
            ["contract.pdf"],
        )

    def test_xml_attachments_removed(self):
        """The XML is flagged when it holds an attachment removed from the list."""
        invoice = self._create_invoice(self.attachment)
        self._generate_xml(invoice)
        self.assertFalse(invoice.l10n_it_edi_ext_xml_attachments_removed)

        invoice.l10n_it_edi_ext_doc_attachment_ids = [
            Command.unlink(self.attachment.id)
        ]
        self.assertTrue(invoice.l10n_it_edi_ext_xml_attachments_removed)
        self.assertFalse(invoice.l10n_it_edi_ext_xml_attachments_missing)

    def test_xml_attachments_missing_and_removed(self):
        """Both flags are set when the list and the XML differ both ways."""
        other = self.env["ir.attachment"].create(
            {"name": "annex.pdf", "raw": b"%PDF-1.4 annex"}
        )
        invoice = self._create_invoice(self.attachment)
        self._generate_xml(invoice)
        invoice.l10n_it_edi_ext_doc_attachment_ids = [Command.set(other.ids)]
        self.assertTrue(invoice.l10n_it_edi_ext_xml_attachments_missing)
        self.assertTrue(invoice.l10n_it_edi_ext_xml_attachments_removed)

    def test_xml_attachments_invoice_pdf_ignored(self):
        """The invoice PDF added by l10n_it_edi is not flagged as removed."""
        invoice = self._create_invoice(self.attachment)
        pdf_values = {
            "name": invoice._get_invoice_report_filename(),
            "raw": b"%PDF-1.4 invoice",
        }
        self._generate_xml(invoice, pdf_values=pdf_values)
        self.assertEqual(len(invoice.l10n_it_edi_ext_xml_attachments_data), 2)
        self.assertFalse(invoice.l10n_it_edi_ext_xml_attachments_removed)
        self.assertFalse(invoice.l10n_it_edi_ext_xml_attachments_missing)

    def test_xml_attachments_vendor_bill(self):
        """The attachments of a vendor bill XML are shown, without warnings."""
        invoice = self._create_invoice(self.attachment)
        xml = invoice._l10n_it_edi_render_xml()
        bill = self.env["account.move"].create(
            {"move_type": "in_invoice", "partner_id": self.italian_partner_a.id}
        )
        bill.l10n_it_edi_attachment_file = base64.b64encode(xml)
        self.assertTrue(bill.l10n_it_edi_ext_xml_generated)
        self.assertEqual(
            [att["name"] for att in bill.l10n_it_edi_ext_xml_attachments_data],
            ["contract.pdf"],
        )
        self.assertFalse(bill.l10n_it_edi_ext_xml_attachments_removed)
        self.assertFalse(bill.l10n_it_edi_ext_xml_attachments_missing)

    def test_xml_attachments_uploaded_bill(self):
        """The attachments of a vendor bill uploaded by hand are shown.

        The uploaded file is kept as the imported e-bill, not as the e-invoice
        XML of the bill.
        """
        self.module = "l10n_it_edi_extension"
        bill = self._assert_import_invoice("IT02780790107_11004.xml", [{}])
        self.assertTrue(bill.l10n_it_edi_ext_attachment_in_id)
        self.assertTrue(bill.l10n_it_edi_ext_xml_generated)
        self.assertEqual(
            [
                (att["name"], att["description"])
                for att in bill.l10n_it_edi_ext_xml_attachments_data
            ],
            [("test.png", "descrizione test")],
        )
        name, mimetype, content = bill._l10n_it_edi_ext_get_xml_attachment_file(0)
        self.assertEqual(name, "test.png")
        self.assertEqual(mimetype, "image/png")
        self.assertTrue(content.startswith(b"\x89PNG"))

    def test_xml_attachments_signed_bill(self):
        """A signed e-bill (.p7m) is read without its signature."""
        path = "l10n_it_edi_extension/tests/import_xmls/IT05979361218_003.xml.p7m"
        with tools.file_open(path, mode="rb") as fd:
            signed = self.env["ir.attachment"].create(
                {"name": "IT05979361218_003.xml.p7m", "raw": fd.read()}
            )
        bill = self.env["account.move"].create(
            {"move_type": "in_invoice", "partner_id": self.italian_partner_a.id}
        )
        bill.l10n_it_edi_ext_attachment_in_id = signed
        tree = bill._l10n_it_edi_ext_get_xml_tree()
        self.assertIsNotNone(tree)
        self.assertEqual(etree.QName(tree).localname, "FatturaElettronica")

    def test_xml_attachment_file(self):
        """An attachment can be read back from the generated XML."""
        invoice = self._create_invoice(self.attachment)
        xml = invoice._l10n_it_edi_render_xml()
        invoice.l10n_it_edi_attachment_file = base64.b64encode(xml)
        name, mimetype, content = invoice._l10n_it_edi_ext_get_xml_attachment_file(0)
        self.assertEqual(name, "contract.pdf")
        self.assertEqual(mimetype, "application/pdf")
        self.assertEqual(content, b"%PDF-1.4 test")
        self.assertIsNone(invoice._l10n_it_edi_ext_get_xml_attachment_file(1))

    def test_xml_attachment_unsafe_mimetype(self):
        """Files the browser could execute are served as generic binaries."""
        move = self.env["account.move"]
        for name in ("page.html", "image.svg", "script.js", "noext"):
            self.assertEqual(
                move._l10n_it_edi_ext_xml_attachment_mimetype(name, False),
                "application/octet-stream",
            )
        self.assertEqual(
            move._l10n_it_edi_ext_xml_attachment_mimetype("scan.jpg", "JPG"),
            "image/jpeg",
        )

    def test_migrate_doc_attachments_from_18(self):
        """The e-invoice attachments of 18.0 are moved to the list.

        Only those of customer invoices, and not the invoice PDF of 16.0.
        """
        invoice = self._create_invoice(post=False)
        bill = self.env["account.move"].create(
            {"move_type": "in_invoice", "partner_id": self.italian_partner_a.id}
        )
        invoice_pdf, bill_file = self.env["ir.attachment"].create(
            [
                {"name": "invoice.pdf", "raw": b"%PDF-1.4 invoice"},
                {"name": "bill.pdf", "raw": b"%PDF-1.4 bill"},
            ]
        )
        # In 18.0 the files are linked to their invoice
        (self.attachment | invoice_pdf).write(
            {"res_model": "account.move", "res_id": invoice.id}
        )
        bill_file.write({"res_model": "account.move", "res_id": bill.id})
        self.env.flush_all()
        # Tables of l10n_it_edi.attachment (18.0) and of l10n_it_fatturapa (16.0)
        self.env.cr.execute(
            """
            CREATE TABLE l10n_it_edi_attachment (
                id serial PRIMARY KEY,
                ir_attachment_id integer,
                invoice_id integer,
                compression varchar,
                format varchar
            );
            CREATE TABLE fatturapa_attachments (
                id serial PRIMARY KEY,
                ir_attachment_id integer,
                invoice_id integer,
                is_pdf_invoice_print boolean
            )
            """
        )
        self.env.cr.execute(
            """
            INSERT INTO l10n_it_edi_attachment (ir_attachment_id, invoice_id)
            VALUES (%(file)s, %(invoice)s), (%(pdf)s, %(invoice)s),
                (%(bill_file)s, %(bill)s);
            INSERT INTO fatturapa_attachments
                (ir_attachment_id, invoice_id, is_pdf_invoice_print)
            VALUES (%(file)s, %(invoice)s, false), (%(pdf)s, %(invoice)s, true)
            """,
            {
                "file": self.attachment.id,
                "pdf": invoice_pdf.id,
                "bill_file": bill_file.id,
                "invoice": invoice.id,
                "bill": bill.id,
            },
        )

        migration = load_script(
            "l10n_it_edi_extension/migrations/19.0.1.0.0/post-migration.py",
            "l10n_it_edi_extension_post_migration",
        )
        migration.migrate(self.env.cr, "18.0.1.0.0")
        self.env.invalidate_all()

        self.assertEqual(invoice.l10n_it_edi_ext_doc_attachment_ids, self.attachment)
        self.assertEqual(self.attachment.res_field, DOC_ATTACHMENT_FIELD)
        self.assertFalse(invoice_pdf.res_field)
        self.assertFalse(bill.l10n_it_edi_ext_doc_attachment_ids)
        self.assertFalse(bill_file.res_field)
