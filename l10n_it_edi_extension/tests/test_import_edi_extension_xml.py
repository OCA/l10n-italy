#  Copyright 2024 Simone Rubino - Aion Tech
#  Copyright 2025 Simone Rubino
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date
from unittest.mock import patch

from odoo import tools
from odoo.exceptions import MissingError

from .common import Common


class TestFatturaPAXMLValidation(Common):
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
        self.assertEqual(move.partner_id.street, "Viale Roma 543")
        self.assertEqual(move.partner_id.state_id.code, "SS")
        self.assertEqual(move.partner_id.country_id.code, "IT")
        self.assertEqual(move.partner_id.vat, "IT02780790107")
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
        zip_name = "xml_import.zip"
        moves = self._import_moves_from_zip(zip_name)

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

    def test_min_import_detail_level_with_line_access(self):
        """If import detail level is Minimum and another module
        tries to access deleted line fields (like l10n_it_edi_withholding does),
        no MissingError should occur thanks to the fix."""
        # Arrange
        company = self.company
        company.l10n_it_edi_import_detail_level = "min"

        # Simulate what l10n_it_edi_withholding does: access move_line_form.price_unit
        original_method = self.env["account.move"]._l10n_it_edi_import_line
        test_case = self

        def patched_import_line(self, element, move_line_form, extra_info=None):
            messages = original_method(element, move_line_form, extra_info)
            # This is what causes the MissingError without the fix:
            # l10n_it_edi_withholding accesses move_line_form.price_unit at line 320
            try:
                _ = move_line_form.price_unit
            except MissingError:
                # Without the fix, this would raise MissingError
                test_case.fail(
                    "MissingError: line was deleted but accessed by another module"
                )
            return messages

        # Act & Assert
        with patch.object(
            type(self.env["account.move"]),
            "_l10n_it_edi_import_line",
            patched_import_line,
        ):
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

    def test_tax_import_detail_level_with_line_access(self):
        """If import detail level is Tax rate and another module
        tries to access deleted line fields (like l10n_it_edi_withholding does),
        no MissingError should occur thanks to the fix."""
        # Arrange
        company = self.company
        company.l10n_it_edi_import_detail_level = "tax"

        # Simulate what l10n_it_edi_withholding does: access move_line_form.price_unit
        original_method = self.env["account.move"]._l10n_it_edi_import_line
        test_case = self

        def patched_import_line(self, element, move_line_form, extra_info=None):
            messages = original_method(element, move_line_form, extra_info)
            # This is what causes the MissingError without the fix
            try:
                _ = move_line_form.price_unit
            except MissingError:
                # Without the fix, this would raise MissingError
                test_case.fail(
                    "MissingError: line was deleted but accessed by another module"
                )
            return messages

        # Act & Assert
        with patch.object(
            type(self.env["account.move"]),
            "_l10n_it_edi_import_line",
            patched_import_line,
        ):
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

    def test_import_zip_tax_detail_level_sale(self):
        """If import detail level is Tax rate,
        and a zip containing a customer invoice is imported,
        the used tax is for customers."""
        # Arrange
        company = self.company
        company.vat = "01654010345"
        company.l10n_it_edi_import_detail_level = "tax"
        zip_name = "INV_2026_00005.zip"

        # Act
        moves = self._import_moves_from_zip(zip_name)

        # Assert
        self.assertEqual(moves.move_type, "out_invoice")
        self.assertEqual(moves.invoice_line_ids.tax_ids.type_tax_use, "sale")

    def test_import_zip_max_detail_level_sale(self):
        """If import detail level is Maximum,
        and a zip containing a customer invoice is imported,
        the used tax is for customers."""
        # Arrange
        company = self.company
        company.vat = "01654010345"
        zip_name = "INV_2026_00005.zip"
        # pre-condition
        self.assertEqual(company.l10n_it_edi_import_detail_level, "max")

        # Act
        moves = self._import_moves_from_zip(zip_name)

        # Assert
        self.assertEqual(moves.move_type, "out_invoice")
        self.assertEqual(moves.invoice_line_ids.tax_ids.type_tax_use, "sale")

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

    def test_preview_link(self):
        """The preview is available for imported bills."""
        # Arrange
        invoice = self._assert_import_invoice(
            "IT02780790107_11004.xml",
            [
                {},
            ],
        )

        # Act
        preview_action = invoice.action_l10n_it_edi_ext_attachment_in_preview()

        # Assert
        self.assertEqual(
            preview_action["url"],
            invoice.l10n_it_edi_ext_attachment_in_preview_link,
        )

    def test_partner_default_product(self):
        """If the partner has a default product and no product is found,
        the partner's default product is used."""
        # Arrange
        supplier = self.env["res.partner"].create(
            {
                "name": "Test supplier",
                "vat": "02780790107",
            }
        )
        default_product = self.default_product.with_company(self.company)
        supplier.l10n_it_edi_ext_default_product_id = default_product

        # Act
        bill = self._assert_import_invoice(
            "IT02780790107_11004.xml",
            [{"partner_id": supplier.id}],
        )

        # Assert
        self.assertRecordValues(
            bill.invoice_line_ids,
            [
                {
                    "product_id": default_product.id,
                    "account_id": default_product.property_account_expense_id.id,
                    "tax_ids": default_product.supplier_taxes_id.ids,
                    "price_total": 6.10,
                },
                {
                    "product_id": default_product.id,
                    "account_id": default_product.property_account_expense_id.id,
                    "tax_ids": default_product.supplier_taxes_id.ids,
                    "price_total": 24.40,
                },
            ],
        )

    def test_partner_default_product_tax_detail_level(self):
        """If the partner has a default product and no product is found,
        and the invoice is imported with "Tax" detail level,
        the partner's default product is used."""
        # Arrange
        supplier = self.env["res.partner"].create(
            {
                "name": "Test supplier",
                "vat": "02780790107",
                "l10n_it_edi_import_detail_level": "tax",
            }
        )
        default_product = self.default_product.with_company(self.company)
        supplier.l10n_it_edi_ext_default_product_id = default_product

        # Act
        bill = self._assert_import_invoice(
            "IT02780790107_11004.xml",
            [{"partner_id": supplier.id}],
        )

        # Assert
        self.assertRecordValues(
            bill.invoice_line_ids,
            [
                {
                    "product_id": default_product.id,
                    "account_id": default_product.property_account_expense_id.id,
                    "tax_ids": default_product.supplier_taxes_id.ids,
                    "price_total": 41.48,
                },
            ],
        )

    def test_import_wrong_company(self):
        """If the invoice is not of current company,
        there is no exception during parsing"""
        # Arrange
        company = self.company
        company.l10n_it_codice_fiscale = False

        # Act
        invoice = self._assert_import_invoice(
            "IT02780790107_11004.xml",
            [
                {},
            ],
        )

        # Assert
        error_message = invoice.message_ids.filtered(
            lambda message: "Error importing attachment" in (message.body or "")
        )
        self.assertFalse(error_message)
