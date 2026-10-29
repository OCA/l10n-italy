#  Copyright 2024 Simone Rubino - Aion Tech
#  Copyright 2025 Simone Rubino
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
import io
import zipfile
from datetime import date
from unittest.mock import patch

from odoo import Command, fields, tools
from odoo.exceptions import MissingError
from odoo.tests import HttpCase, new_test_user
from odoo.tools import file_open, mute_logger

from .common import Common


class TestFatturaPAXMLValidation(Common):
    def test_02_xml_import(self):
        move = self._assert_import_invoice("IT02780790107_11005.xml", [{}])
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
        move = self._assert_import_invoice("IT05979361218_003.xml", [{}])
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
        move = self._assert_import_invoice("IT02780790107_11004.xml", [{}])
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
        edi_attachment = move.message_ids.attachment_ids.filtered(
            lambda a: a.name == "test.png"
        )
        orig_attachment_path = tools.misc.file_path(
            "l10n_it_edi_extension/tests/import_xmls/test.png"
        )
        with open(orig_attachment_path, "rb") as orig_attachment:
            orig_attachment_data = orig_attachment.read()
            self.assertEqual(edi_attachment.raw, orig_attachment_data)

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
            attachment_name = out_move.l10n_it_edi_attachment_name
            expected_invoices_values = check_invoices_values.get(attachment_name)
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
        company.l10n_it_codice_fiscale = "01654010345"
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
        company.l10n_it_codice_fiscale = "01654010345"
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
                "vat": "IT02780790107",
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

        # Assert
        self.assertTrue(invoice.l10n_it_edi_ext_attachment_in_id)

    def test_imported_attachment(self):
        """The imported e-invoice is linked to the bill without duplicating it,
        and the copies of the bill are not linked to it."""
        # Arrange
        invoice = self._assert_import_invoice(
            "IT02780790107_11004.xml",
            [
                {},
            ],
        )
        imported_attachment = invoice.l10n_it_edi_ext_attachment_in_id

        # Act
        invoice_copy = invoice.copy()

        # Assert
        self.assertEqual(
            self.env["ir.attachment"].search_count(
                [
                    ("res_model", "=", invoice._name),
                    ("res_id", "=", invoice.id),
                    ("name", "=", imported_attachment.name),
                ]
            ),
            1,
        )
        self.assertFalse(invoice_copy.l10n_it_edi_ext_attachment_in_id)

    def test_partner_default_product(self):
        """If the partner has a default product and no product is found,
        the partner's default product is used."""
        # Arrange
        supplier = self.env["res.partner"].create(
            {
                "name": "Test supplier",
                "vat": "IT02780790107",
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
                "vat": "IT02780790107",
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

    def test_receive_signed_vendor_bill(self):
        """Test a signed (P7M) sample e-invoice file from
        https://www.fatturapa.gov.it/export/documenti/fatturapa/v1.2/IT01234567890_FPR01.xml

        Note: this is the SAME test (code is identical on purpose) found in
        odoo/addons/l10n_it_edi/tests/test_edi_import.py
        but IT01234567890_FPR01.xml.p7m is actually a base64-encoded text file.
        """
        self._assert_import_invoice(
            "IT01234567890_FPR01.xml.p7m",
            [
                {
                    "ref": "01234567890",
                    "invoice_date": fields.Date.from_string("2014-12-18"),
                    "amount_untaxed": 5.0,
                    "amount_tax": 1.1,
                    "invoice_line_ids": [
                        {
                            "quantity": 5.0,
                            "price_unit": 1.0,
                        }
                    ],
                }
            ],
        )


class TestIsL10nItEdiImportFile(Common):
    """Cover ``account.move._is_l10n_it_edi_import_file``."""

    def _create_attachment(self, name, raw, mimetype=False):
        """Create an ``ir.attachment`` with the given name and content.

        ``mimetype`` may be set to a known value to bypass ``guess_mimetype``;
        otherwise the attachment is left for Odoo to compute.
        """
        values = {
            "name": name,
            "raw": raw,
            "type": "binary",
        }
        if mimetype is not False:
            values["mimetype"] = mimetype
        return self.env["ir.attachment"].create(values)

    def _is_l10n_it_edi_import_file(self, attachment):
        move_model = self.env["account.move"]
        file_data = move_model._to_files_data(attachment)[0]
        return move_model._is_l10n_it_edi_import_file(file_data)

    def test_super_recognises_xml(self):
        """When Odoo core already recognises the file, the result is kept."""
        path = "l10n_it_edi_extension/tests/import_xmls/IT01234567890_FPR03.xml"
        with file_open(path, mode="rb") as fd:
            attachment = self._create_attachment("IT01234567890_FPR03.xml", fd.read())
        self.assertTrue(attachment.mimetype, "Mimetype should be auto-detected")
        self.assertTrue(self._is_l10n_it_edi_import_file(attachment))

    def test_p7m_with_undetected_mimetype_is_recognised(self):
        """``.p7m`` files whose mimetype is ``application/octet-stream``
        (because ``guess_mimetype`` cannot detect CAdES) are still recognised
        thanks to the extension's signature-stripping fallback.
        """
        path = "l10n_it_edi_extension/tests/import_xmls/IT05979361218_003.xml.p7m"
        with file_open(path, mode="rb") as fd:
            raw = fd.read()
        attachment = self._create_attachment(
            "IT05979361218_003.xml.p7m", raw, mimetype="application/octet-stream"
        )
        self.assertTrue(self._is_l10n_it_edi_import_file(attachment))

    def test_p7m_with_invalid_content_is_not_recognised(self):
        """``.p7m`` whose contents cannot be parsed as a FatturaElettronica
        is rejected by the extension's fallback.
        """
        attachment = self._create_attachment(
            "bogus.p7m",
            b"not a valid signed e-invoice",
            mimetype="application/octet-stream",
        )
        self.assertFalse(self._is_l10n_it_edi_import_file(attachment))

    def test_non_p7m_with_undetected_mimetype_is_not_recognised(self):
        """The fallback only triggers for ``.p7m`` files."""
        attachment = self._create_attachment(
            "random.bin",
            b"random binary data",
            mimetype="application/octet-stream",
        )
        self.assertFalse(self._is_l10n_it_edi_import_file(attachment))

    def test_empty_raw_is_not_recognised(self):
        """Empty content with a ``.p7m`` name is rejected (no raw to parse)."""
        attachment = self.env["ir.attachment"].create(
            {
                "name": "empty.p7m",
                "type": "binary",
            }
        )
        self.assertFalse(self._is_l10n_it_edi_import_file(attachment))


class TestImportWizardSplitting(Common):
    # Cover l10n_it_edi.import_file_wizard.action_import for multiple e-invoices
    # in one file, and for multiple files in one zip

    def _build_zip(self, members):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for arcname, data in members.items():
                zf.writestr(arcname, data)
        return base64.b64encode(buf.getvalue())

    def _run_wizard(self, zip_name, zip_bytes):
        wizard = (
            self.env["l10n_it_edi.import_file_wizard"]
            .with_company(self.company)
            .create(
                {
                    "l10n_it_edi_attachment_filename": zip_name,
                    "l10n_it_edi_attachment": zip_bytes,
                }
            )
        )
        action = wizard.action_import()
        return self.env["account.move"].search(action["domain"])

    def test_multi_body_xml_in_zip_creates_one_invoice_per_body(self):
        path = "l10n_it_edi_extension/tests/import_xmls/IT01234567890_FPR03.xml"
        with file_open(path, mode="rb") as fd:
            xml_bytes = fd.read()
        zip_bytes = self._build_zip({"IT01234567890_FPR03.xml": xml_bytes})
        # FPR03's CedentePrestatore CodiceFiscale is 03533590174.
        self.company.l10n_it_codice_fiscale = "03533590174"
        moves = self._run_wizard("multi_body.zip", zip_bytes)
        # IT01234567890_FPR03.xml has 2 bodies with refs 123 and 456.
        self.assertEqual(len(moves), 2)
        self.assertEqual(
            sorted(moves.mapped("ref")),
            ["123", "456"],
        )
        # Each created move is linked to its own e-invoice.
        self.assertEqual(
            sorted(moves.l10n_it_edi_ext_attachment_in_id.mapped("name")),
            ["IT01234567890_FPR03.xml", "IT01234567890_FPR03_2.xml"],
        )

    def test_single_body_xml_in_zip_creates_one_invoice(self):
        path = "l10n_it_edi_extension/tests/import_xmls/IT02780790107_11004.xml"
        with file_open(path, mode="rb") as fd:
            xml_bytes = fd.read()
        zip_bytes = self._build_zip({"IT02780790107_11004.xml": xml_bytes})
        moves = self._run_wizard("single_body.zip", zip_bytes)
        self.assertEqual(len(moves), 1)

    def test_p7m_with_undetected_mimetype_in_zip(self):
        path = "l10n_it_edi_extension/tests/import_xmls/IT05979361218_003.xml.p7m"
        with file_open(path, mode="rb") as fd:
            p7m_bytes = fd.read()
        zip_bytes = self._build_zip({"IT05979361218_003.xml.p7m": p7m_bytes})
        moves = self._run_wizard("signed.zip", zip_bytes)
        self.assertTrue(moves)
        self.assertEqual(
            moves.l10n_it_edi_ext_attachment_in_id.name, "IT05979361218_003.xml.p7m"
        )

    def test_zip_with_multi_and_single_invoices(self):
        multi_path = "l10n_it_edi_extension/tests/import_xmls/IT01234567890_FPR03.xml"
        single_path = "l10n_it_edi_extension/tests/import_xmls/IT02780790107_11004.xml"
        with file_open(multi_path, mode="rb") as fd:
            multi_bytes = fd.read()
        with file_open(single_path, mode="rb") as fd:
            single_bytes = fd.read()
        zip_bytes = self._build_zip(
            {
                "IT01234567890_FPR03.xml": multi_bytes,
                "IT02780790107_11004.xml": single_bytes,
            }
        )
        moves = self._run_wizard("mixed.zip", zip_bytes)
        # must be 3 invoices in total
        self.assertEqual(len(moves), 3)


class TestFatturaPAPreview(Common, HttpCase):
    @mute_logger("odoo.http")
    def test_preview_access(self):
        """Only users that can read the bill get the preview of its e-invoice."""
        # Arrange
        invoice = self._assert_import_invoice(
            "IT02780790107_11004.xml",
            [
                {},
            ],
        )
        preview_url = f"/fatturapa/preview/{invoice.id}"
        other_company = self.company_data["company"]
        other_company_user = new_test_user(
            self.env,
            login="other_company_user",
            groups="account.group_account_invoice",
            company_id=other_company.id,
            company_ids=[Command.set(other_company.ids)],
        )
        # pre-condition
        self.assertNotEqual(invoice.company_id, other_company)

        # Act
        self.authenticate(other_company_user.login, other_company_user.login)
        other_company_response = self.url_open(preview_url)
        self.authenticate(self.env.user.login, self.env.user.login)
        user_response = self.url_open(preview_url)

        # Assert
        self.assertEqual(other_company_response.status_code, 403)
        self.assertEqual(user_response.status_code, 200)
        self.assertEqual(user_response.headers["Content-Type"], "application/pdf")
