# Copyright 2025 Simone Rubino
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command, tests, tools

from .common import Common


class TestExport(Common):
    def test_narration(self):
        """The narration included in the invoice
        is exported to the XML in Causale nodes."""
        invoice = self.init_invoice(
            "out_invoice",
            amounts=[100],
            company=self.company,
            partner=self.italian_partner_a,
            taxes=self.default_tax,
        )
        invoice.invoice_date_due = invoice.date
        invoice.narration = "first line\n\nsecond line"
        invoice.action_post()
        self._assert_export_invoice(invoice, "narration.xml")

    def test_invoice_causale_non_latin(self):
        narration = """
            <p> </p>
            <p>```</p>
            <p>L’impresa è un’attività economica organizzata ai fini della produzione
             o dello scambio di beni o servizi.</p>
            <p>Importo totale fattura è 976,49 €.</p>
            <p>```</p>
        """
        invoice = (
            self.env["account.move"]
            .with_company(self.company)
            .create(
                {
                    "move_type": "out_invoice",
                    "invoice_date": "2022-03-24",
                    "invoice_date_due": "2022-03-24",
                    "partner_id": self.italian_partner_a.id,
                    "narration": narration,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "line1",
                                "price_unit": 800.40,
                                "tax_ids": [Command.set(self.default_tax.ids)],
                            }
                        ),
                    ],
                }
            )
        )
        invoice.action_post()
        self._assert_export_invoice(invoice, "test_invoice_causale_non_latin.xml")

    def test_partner_shipping(self):
        """The partner shipping included in the invoice
        is exported to the XML in IndirizzoResa node."""
        invoice = self.init_invoice(
            "out_invoice",
            amounts=[100],
            company=self.company,
            partner=self.italian_partner_a,
            taxes=self.default_tax,
        )
        invoice.invoice_date_due = invoice.date
        invoice.partner_shipping_id = self.italian_shipping_partner_a
        invoice.action_post()
        self._assert_export_invoice(invoice, "partner_shipping.xml")

    def test_partner_shipping_with_related_documents(self):
        """Sequence tag in IndirizzoResa node."""
        invoice = self.init_invoice(
            "out_invoice",
            amounts=[100],
            company=self.company,
            partner=self.italian_partner_b,
            taxes=self.split_payment_tax,
        )
        invoice.invoice_date_due = invoice.date
        invoice.l10n_it_origin_document_type = "purchase_order"
        invoice.l10n_it_origin_document_date = invoice.date
        invoice.l10n_it_origin_document_name = "PO0123"
        invoice.l10n_it_cup = "0123456789"
        invoice.l10n_it_cig = "0987654321"
        invoice.partner_shipping_id = self.italian_shipping_partner_a
        invoice.action_post()
        self._assert_export_invoice(invoice, "partner_shipping_sequence.xml")

    def test_us_partner_shipping(self):
        """The US partner shipping included in the invoice
        is exported to the XML in IndirizzoResa node."""
        usd = self.env.ref("base.USD")

        self.env["res.currency.rate"].with_company(self.company).create(
            {
                "name": "2024-08-06",
                "rate": 1.0789,
                "currency_id": usd.id,
            }
        )

        invoice = (
            self.env["account.move"]
            .with_company(self.company)
            .create(
                {
                    "move_type": "out_invoice",
                    "invoice_date": "2024-08-07",
                    "invoice_date_due": "2024-08-07",
                    "partner_id": self.us_partner.id,
                    "partner_shipping_id": self.us_shipping_partner.id,
                    "currency_id": usd.id,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "A productive product",
                                "price_unit": 1068.11,
                                "quantity": 1,
                                "tax_ids": [Command.set(self.tax_zero_percent_us.ids)],
                            }
                        ),
                    ],
                }
            )
        )
        invoice.action_post()
        self._assert_export_invoice(invoice, "us_partner_shipping.xml")

    def test_hide_descriptive_lines_simplified(self):
        """Check that descriptive lines are hidden in the simplified e-invoice
        according to invoice/partner/company configuration."""
        # Arrange
        invoice = self.init_invoice(
            "out_invoice",
            partner=self.italian_partner_no_address_codice,
            amounts=[
                100,
            ],
            company=self.company,
        )
        self.assertTrue(invoice._l10n_it_edi_is_simplified())
        self._assert_descriptive_lines_hidden(invoice)

    def test_hide_descriptive_lines(self):
        """Check that descriptive lines are hidden in the e-invoice
        according to invoice/partner/company configuration."""
        # Arrange
        invoice = self.init_invoice(
            "out_invoice",
            partner=self.italian_partner_b,
            amounts=[
                100,
            ],
            company=self.company,
        )
        self.assertFalse(invoice._l10n_it_edi_is_simplified())
        self._assert_descriptive_lines_hidden(invoice)

    def _assert_descriptive_lines_hidden(self, invoice):
        """Check that notes and sections are hidden
        according to the configuration for `invoice`."""
        note_name = "Test note"
        section_name = "Test section"
        with tests.Form(invoice) as invoice_form:
            with invoice_form.invoice_line_ids.new() as section_line:
                section_line.name = section_name
                section_line.display_type = "line_section"
            with invoice_form.invoice_line_ids.new() as note_line:
                note_line.name = note_name
                note_line.display_type = "line_note"
        # Map settings for
        # invoice, partner, company
        # to their expected result
        hide_keys_dict = {
            (False, False, False): "nothing hidden",
            ("none", False, False): "nothing hidden",
            ("note", False, False): "notes hidden",
            ("section", False, False): "sections hidden",
            ("note_section", False, False): "both hidden",
            (False, "note", False): "notes hidden",
            (False, False, "note"): "notes hidden",
            ("none", False, "note"): "nothing hidden",
        }

        for hide_keys, expected_result in hide_keys_dict.items():
            (
                invoice.l10n_it_edi_hide_line_type,
                invoice.partner_id.l10n_it_edi_hide_line_type,
                invoice.company_id.l10n_it_edi_hide_line_type,
            ) = hide_keys
            invoice.action_post()

            # Act
            e_invoice_content = invoice._l10n_it_edi_render_xml().decode()

            # Assert
            if expected_result == "nothing hidden":
                self.assertIn(note_name, e_invoice_content)
                self.assertIn(section_name, e_invoice_content)
            elif expected_result == "notes hidden":
                self.assertNotIn(note_name, e_invoice_content)
                self.assertIn(section_name, e_invoice_content)
            elif expected_result == "sections hidden":
                self.assertIn(note_name, e_invoice_content)
                self.assertNotIn(section_name, e_invoice_content)
            elif expected_result == "both hidden":
                self.assertNotIn(note_name, e_invoice_content)
                self.assertNotIn(section_name, e_invoice_content)
            else:
                self.fail(f"Expected result {expected_result} not managed")

            # cleanup for next loop,
            # without spamming the logs with deleted mail.followers etc.
            with tools.mute_logger("odoo.models.unlink"):
                invoice.button_draft()
