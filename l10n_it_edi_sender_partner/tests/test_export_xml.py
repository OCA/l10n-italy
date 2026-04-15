# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.l10n_it_edi.tests.common import TestItEdi


class TestItEdiExport(TestItEdi):
    """Test export of invoice with sender partner"""

    def test_export_with_sender(self):
        """Test that TerzoIntermediarioOSoggettoEmittente is in the XML"""
        sender = self.env["res.partner"].create(
            {
                "name": "Intermediario Srl",
                "vat": "IT12345670017",
                "country_id": self.env.ref("base.it").id,
            }
        )
        self.company.l10n_edi_it_sender_partner = sender

        invoice = (
            self.env["account.move"]
            .with_company(self.company)
            .create(
                {
                    "move_type": "out_invoice",
                    "partner_id": self.italian_partner_a.id,
                    "invoice_date": "2024-01-15",
                    "invoice_line_ids": [
                        (
                            0,
                            0,
                            {
                                "name": "Test product",
                                "quantity": 1,
                                "price_unit": 100.0,
                                "tax_ids": [(6, 0, self.default_tax.ids)],
                            },
                        )
                    ],
                }
            )
        )
        invoice.action_post()

        xml_content = invoice._l10n_it_edi_render_xml().decode()

        self.assertIn("TerzoIntermediarioOSoggettoEmittente", xml_content)
        self.assertIn("12345670017", xml_content)
        self.assertIn("<SoggettoEmittente>TZ</SoggettoEmittente>", xml_content)
