# Copyright 2025 Nextev Srl
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date

from odoo.exceptions import ValidationError
from odoo.tests import tagged

from .common import Common


@tagged("-at_install", "post_install")
class TestAltriDatiGestionali(Common):
    """Tests for AltriDatiGestionali (2.2.1.16) export on invoice lines."""

    def test_model_creation_with_text_ref(self):
        """Test creating other data with only text reference."""
        invoice = self.init_invoice(
            "out_invoice",
            amounts=[100],
            company=self.company,
            partner=self.italian_partner_a,
            taxes=self.default_tax,
        )
        line = invoice.invoice_line_ids[0]
        other_data = self.env["l10n_it_edi.line_other_data"].create(
            {
                "move_line_id": line.id,
                "name": "TIPO1",
                "text_ref": "Test Reference",
            }
        )
        self.assertEqual(other_data.name, "TIPO1")
        self.assertEqual(other_data.text_ref, "Test Reference")
        self.assertFalse(other_data.num_ref)
        self.assertFalse(other_data.date_ref)

    def test_model_creation_with_num_ref(self):
        """Test creating other data with only numeric reference."""
        invoice = self.init_invoice(
            "out_invoice",
            amounts=[100],
            company=self.company,
            partner=self.italian_partner_a,
            taxes=self.default_tax,
        )
        line = invoice.invoice_line_ids[0]
        other_data = self.env["l10n_it_edi.line_other_data"].create(
            {
                "move_line_id": line.id,
                "name": "TIPO2",
                "num_ref": 123.45678901,
            }
        )
        self.assertEqual(other_data.name, "TIPO2")
        self.assertAlmostEqual(other_data.num_ref, 123.45678901, places=8)

    def test_model_creation_with_date_ref(self):
        """Test creating other data with only date reference."""
        invoice = self.init_invoice(
            "out_invoice",
            amounts=[100],
            company=self.company,
            partner=self.italian_partner_a,
            taxes=self.default_tax,
        )
        line = invoice.invoice_line_ids[0]
        test_date = date(2024, 6, 15)
        other_data = self.env["l10n_it_edi.line_other_data"].create(
            {
                "move_line_id": line.id,
                "name": "TIPO3",
                "date_ref": test_date,
            }
        )
        self.assertEqual(other_data.name, "TIPO3")
        self.assertEqual(other_data.date_ref, test_date)

    def test_model_creation_all_refs(self):
        """Test creating other data with all references."""
        invoice = self.init_invoice(
            "out_invoice",
            amounts=[100],
            company=self.company,
            partner=self.italian_partner_a,
            taxes=self.default_tax,
        )
        line = invoice.invoice_line_ids[0]
        test_date = date(2024, 12, 31)
        other_data = self.env["l10n_it_edi.line_other_data"].create(
            {
                "move_line_id": line.id,
                "name": "ALLTYPES",
                "text_ref": "All refs",
                "num_ref": 999.12345678,
                "date_ref": test_date,
            }
        )
        self.assertEqual(other_data.name, "ALLTYPES")
        self.assertEqual(other_data.text_ref, "All refs")
        self.assertAlmostEqual(other_data.num_ref, 999.12345678, places=8)
        self.assertEqual(other_data.date_ref, test_date)

    def test_validation_no_ref_provided(self):
        """Test validation error when no reference is provided."""
        invoice = self.init_invoice(
            "out_invoice",
            amounts=[100],
            company=self.company,
            partner=self.italian_partner_a,
            taxes=self.default_tax,
        )
        line = invoice.invoice_line_ids[0]
        with self.assertRaises(ValidationError):
            self.env["l10n_it_edi.line_other_data"].create(
                {
                    "move_line_id": line.id,
                    "name": "NOTYPE",
                }
            )

    def test_export_altri_dati_gestionali(self):
        """Test that AltriDatiGestionali is exported into XML."""
        invoice = self.init_invoice(
            "out_invoice",
            amounts=[100],
            company=self.company,
            partner=self.italian_partner_a,
            taxes=self.default_tax,
        )
        invoice.invoice_date_due = invoice.date
        # Clear delivery address to avoid DatiTrasporto in XML
        invoice.partner_shipping_id = False
        line = invoice.invoice_line_ids[0]

        # Create other data entries
        test_date = date(2024, 6, 15)
        self.env["l10n_it_edi.line_other_data"].create(
            {
                "move_line_id": line.id,
                "name": "CODLAV",
                "text_ref": "LAV123",
            }
        )
        self.env["l10n_it_edi.line_other_data"].create(
            {
                "move_line_id": line.id,
                "name": "NUMORD",
                "num_ref": 12345.67,
                "date_ref": test_date,
            }
        )

        invoice.action_post()
        self._assert_export_invoice(invoice, "altri_dati_gestionali.xml")

    def test_one2many_relationship(self):
        """Test the One2many relationship between move line and other data."""
        invoice = self.init_invoice(
            "out_invoice",
            amounts=[100],
            company=self.company,
            partner=self.italian_partner_a,
            taxes=self.default_tax,
        )
        line = invoice.invoice_line_ids[0]

        # Initially, no other data
        self.assertEqual(len(line.l10n_it_edi_other_data_ids), 0)

        # Create two entries
        self.env["l10n_it_edi.line_other_data"].create(
            {
                "move_line_id": line.id,
                "name": "TIPO1",
                "text_ref": "First",
            }
        )
        self.env["l10n_it_edi.line_other_data"].create(
            {
                "move_line_id": line.id,
                "name": "TIPO2",
                "num_ref": 42.0,
            }
        )

        # Check relationship
        self.assertEqual(len(line.l10n_it_edi_other_data_ids), 2)

    def test_copy_invoice_with_other_data(self):
        """Test that duplicating invoice copies other data entries."""
        invoice = self.init_invoice(
            "out_invoice",
            amounts=[100],
            company=self.company,
            partner=self.italian_partner_a,
            taxes=self.default_tax,
        )
        line = invoice.invoice_line_ids[0]

        # Create other data entry
        self.env["l10n_it_edi.line_other_data"].create(
            {
                "move_line_id": line.id,
                "name": "COPY",
                "text_ref": "Should be copied",
            }
        )

        # Duplicate invoice
        invoice_copy = invoice.copy()

        # Verify the other data is copied
        copy_line = invoice_copy.invoice_line_ids[0]
        self.assertEqual(len(copy_line.l10n_it_edi_other_data_ids), 1)
        self.assertEqual(copy_line.l10n_it_edi_other_data_ids[0].name, "COPY")
        self.assertEqual(
            copy_line.l10n_it_edi_other_data_ids[0].text_ref, "Should be copied"
        )
