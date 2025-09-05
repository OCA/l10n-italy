#  Copyright 2024 Simone Rubino - Aion Tech
#  Copyright 2025 Simone Rubino
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
from datetime import date

from odoo import tools

from odoo.addons.l10n_it_edi.tests.common import TestItEdi


class TestFatturaPAXMLValidation(TestItEdi):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.module = "l10n_it_edi_extension"
        cls.env.company.l10n_edi_it_create_partner = True
        cls.company.l10n_edi_it_create_partner = True

    def _edi_import_invoice(self, filename):
        moves = self.env["account.move"]
        path = f"l10n_it_edi_extension/tests/import_xmls/{filename}"

        with tools.file_open(path, mode="rb") as file:
            content = file.read()

            attachment = self.env["ir.attachment"].create(
                {
                    "name": filename,
                    "raw": content,
                    "type": "binary",
                }
            )

            if not attachment._is_l10n_it_edi_import_file():
                attachment.unlink()
                return False

            for file_data in attachment._decode_edi_l10n_it_edi(filename, content):
                move = self.env["account.move"].with_company(self.company).create({})
                attachment.write(
                    {
                        "res_model": "account.move",
                        "res_id": move.id,
                        "res_field": "l10n_it_edi_attachment_file",
                    }
                )

                move._l10n_it_edi_import_invoice(move, file_data, True)
                moves |= move

        return moves

    def test_02_xml_import(self):
        move = self._edi_import_invoice("IT02780790107_11005.xml")
        move._extend_with_attachments(move.l10n_it_edi_attachment_id, new=True)
        self.assertEqual(move.ref, "124")
        self.assertEqual(move.partner_id.name, "Societa' Alpha SRL")
        self.assertEqual(move.invoice_line_ids[0].tax_ids[0].name, "22% G")
        self.assertEqual(move.invoice_line_ids[1].tax_ids[0].name, "22% G")
        self.assertEqual(move.invoice_line_ids[0].tax_ids[0].amount, 22)
        self.assertEqual(move.invoice_line_ids[1].tax_ids[0].amount, 22)
        self.assertEqual(move.invoice_line_ids[1].price_unit, 2)
        self.assertTrue(len(move.l10n_it_edi_line_ids) == 2)
        for edi_line in move.l10n_it_edi_line_ids:
            self.assertTrue(edi_line.line_number in (1, 2))
            if edi_line.line_number == 1:
                self.assertEqual(edi_line.l10n_it_edi_article_code_ids[0].name, "EAN")
                self.assertEqual(
                    edi_line.l10n_it_edi_article_code_ids[0].code_val, "12345"
                )

    def test_03_xml_import(self):
        move = self._edi_import_invoice("IT05979361218_003.xml")
        move._extend_with_attachments(move.l10n_it_edi_attachment_id, new=True)
        self.assertEqual(move.ref, "FT/2015/0008")
        self.assertEqual(move.l10n_it_edi_sender, "TZ")
        self.assertEqual(
            move.l10n_it_edi_line_ids[0].l10n_it_edi_discount_rise_price_ids[0].name,
            "SC",
        )
        self.assertEqual(
            move.l10n_it_edi_line_ids[0]
            .l10n_it_edi_discount_rise_price_ids[0]
            .percentage,
            10,
        )
        self.assertEqual(move.amount_untaxed, 9)
        self.assertEqual(move.amount_tax, 0)
        self.assertEqual(move.amount_total, 9)

    def test_04_xml_import(self):
        move = self._edi_import_invoice("IT02780790107_11004.xml")
        move._extend_with_attachments(move.l10n_it_edi_attachment_id, new=True)
        self.assertEqual(move.ref, "123")
        self.assertEqual(len(move.invoice_line_ids[0].tax_ids), 1)
        self.assertEqual(move.invoice_line_ids[0].tax_ids[0].name, "22% G")
        self.assertEqual(move.l10n_it_edi_summary_ids[0].amount_untaxed, 34.00)
        self.assertEqual(move.l10n_it_edi_summary_ids[0].amount_tax, 7.48)
        self.assertEqual(move.l10n_it_edi_summary_ids[0].payability, "D")
        self.assertEqual(move.partner_id.name, "SOCIETA' ALPHA SRL")
        self.assertEqual(move.partner_id.street, "VIALE ROMA 543")
        self.assertEqual(move.partner_id.state_id.code, "SS")
        self.assertEqual(move.partner_id.country_id.code, "IT")
        self.assertEqual(move.partner_id.vat, "02780790107")
        self.assertEqual(
            move.l10n_it_edi_tax_representative_id.name, "Rappresentante fiscale"
        )
        self.assertTrue(move.l10n_edi_it_art73)
        for tag in [
            "DatiOrdineAcquisto",
            "DatiContratto",
            "DatiConvenzione",
            "DatiRicezione",
            "DatiTrasporto",
        ]:
            self.assertTrue(
                any(tag in str(body) for body in move.mapped("message_ids.body")),
                f"'{tag}' not found in message bodies",
            )

        # verify if attached documents are correctly imported
        attachments = self.env["ir.attachment"].search(
            [("res_model", "=", "account.move"), ("res_id", "=", move.id)]
        )
        self.assertEqual(len(attachments), 1)
        orig_attachment_path = tools.misc.file_path(
            "l10n_it_edi_extension/tests/import_xmls/test.png"
        )
        with open(orig_attachment_path, "rb") as orig_attachment:
            orig_attachment_data = orig_attachment.read()
            self.assertEqual(attachments[0].raw, orig_attachment_data)

    def test_import_zip(self):
        path = "l10n_it_edi_extension/tests/import_xmls/xml_import.zip"
        import_file_model = self.env["l10n_it_edi.import_file_wizard"].with_company(
            self.company
        )

        with tools.file_open(path, mode="rb") as file:
            encoded_file = base64.encodebytes(file.read())

            wizard_attachment_import = import_file_model.create(
                {
                    "l10n_it_edi_attachment_filename": "xml_import.zip",
                    "l10n_it_edi_attachment": encoded_file,
                }
            )
            action = wizard_attachment_import.action_import()

        move_ids = action.get("domain")[0][2]
        moves = self.env["account.move"].browse(move_ids)
        out_moves = moves.filtered(lambda m: m.is_sale_document())
        in_moves = moves.filtered(lambda m: m.is_purchase_document())
        self.assertEqual(len(out_moves), 6)
        self.assertEqual(len(in_moves), 36)

        check_invoices_values = {
            "IT06363391001_00012.xml": [
                {
                    "invoice_date": date(
                        2020,
                        month=1,
                        day=7,
                    ),
                    "invoice_date_due": date(
                        2020,
                        month=2,
                        day=29,
                    ),
                },
            ],
            "IT06363391001_00009.xml": [
                {
                    "partner_id": self.env["res.partner"].search(
                        [
                            ("name", "=", "Foreign Customer"),
                        ],
                        limit=1,
                    ),
                }
            ],
        }

        for out_move in out_moves:
            attachment = out_move.l10n_it_edi_attachment_id
            expected_invoices_values = check_invoices_values.get(attachment.name)
            if expected_invoices_values is not None:
                for move, expected_values in zip(
                    out_move,
                    expected_invoices_values,
                    strict=True,
                ):
                    for field, expected_value in expected_values.items():
                        self.assertEqual(
                            getattr(move, field),
                            expected_value,
                            f"Field {field} of invoice {move.display_name} "
                            f"does not match",
                        )

    def test_multiple_invoices(self):
        """If an e-invoice contains multiple invoices, they are all created."""
        # Arrange
        self.company.l10n_it_codice_fiscale = "03533590174"

        # Assert
        self._assert_import_invoice(
            "IT01234567890_FPR03.xml",
            [
                {
                    "ref": "123",
                },
                {
                    "ref": "456",
                },
            ],
        )

    def test_create_partner(self):
        """If partner does not exist, it is created during import."""
        partner_name = "SOCIETA' ALPHA SRL"
        # pre-condition
        partner = self.env["res.partner"].search(
            [
                ("name", "=", partner_name),
            ],
            limit=1,
        )
        self.assertFalse(partner)

        # Act
        invoice = self._assert_import_invoice("IT02780790107_11004.xml", [{}])

        # Assert
        partner = invoice.partner_id
        self.assertEqual(partner.name, partner_name)

    def test_avoid_create_partner(self):
        """Partner is not created during import if the setting is disabled."""
        self.env.company.l10n_edi_it_create_partner = False
        partner_name = "SOCIETA' BETA SRL"
        # pre-condition
        partner = self.env["res.partner"].search(
            [
                ("name", "=", partner_name),
            ],
            limit=1,
        )
        self.assertFalse(partner)

        # Act
        invoice = self._assert_import_invoice("IT02780790107_11004.xml", [{}])

        # Assert
        partner = invoice.partner_id
        self.assertFalse(partner)

    def test_min_import_detail_level(self):
        """If import detail level is Minimum,
        no line is imported."""
        # Arrange
        company = self.company
        company.l10n_it_edi_import_detail_level = "min"

        # Act
        invoice = self._assert_import_invoice(
            "IT02780790107_11004.xml",
            [
                {
                    "company_id": company.id,
                },
            ],
        )

        # Assert
        self.assertFalse(invoice.invoice_line_ids)

    def test_tax_import_detail_level(self):
        """If import detail level is Tax rate,
        summary lines are imported."""
        # Arrange
        company = self.company
        company.l10n_it_edi_import_detail_level = "tax"

        # Act
        invoice = self._assert_import_invoice(
            "IT02780790107_11004.xml",
            [
                {
                    "company_id": company.id,
                },
            ],
        )

        # Assert
        self.assertEqual(len(invoice.invoice_line_ids), 1)

    def test_max_import_detail_level(self):
        """If import detail level is Maximum,
        all lines are imported."""
        # Arrange
        company = self.company
        # pre-condition
        self.assertEqual(company.l10n_it_edi_import_detail_level, "max")

        # Act
        invoice = self._assert_import_invoice(
            "IT02780790107_11004.xml",
            [
                {
                    "company_id": company.id,
                },
            ],
        )

        # Assert
        self.assertEqual(len(invoice.invoice_line_ids), 2)

    def test_partner_import_detail_level(self):
        """If import detail level is Maximum in the Company
        and minimum in the partner,
        the invoice is imported with minimum detail level."""
        # Arrange
        company = self.company
        partner = self.env["res.partner"].create(
            {
                "name": "Test partner",
                "vat": "02780790107",
                "l10n_it_edi_import_detail_level": "min",
            },
        )
        # pre-condition
        self.assertEqual(company.l10n_it_edi_import_detail_level, "max")
        self.assertEqual(partner.l10n_it_edi_import_detail_level, "min")

        # Act
        invoice = self._assert_import_invoice(
            "IT02780790107_11004.xml",
            [
                {
                    "company_id": company.id,
                    "partner_id": partner.id,
                },
            ],
        )

        # Assert
        self.assertFalse(invoice.invoice_line_ids)
