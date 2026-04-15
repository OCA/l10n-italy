# Copyright 2025 Simone Rubino
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command

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
