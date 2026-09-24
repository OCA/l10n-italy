from odoo import fields

from odoo.addons.l10n_it_edi.tests.common import TestItEdi


class TestItEdiImport(TestItEdi):
    """Main test class for the l10n_it_edi vendor bills XML import"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # sender partner atteso nell’XML
        cls.intermediary_partner = cls.env["res.partner"].create(
            {
                "name": "INTERMEDIARIO SRL",
                "vat": "IT12345670017",
                "country_id": cls.env.ref("base.it").id,
            }
        )

    def test_receive_vendor_bill(self):
        """Test a sample e-invoice file with an intermediary"""
        self.module = "l10n_it_edi_sender_partner"
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
        l10n_it_edi_intermediary_id = invoice.l10n_it_edi_intermediary_id
        self.assertTrue(l10n_it_edi_intermediary_id)
        self.assertEqual(l10n_it_edi_intermediary_id.vat, "IT12345670017")
        self.assertEqual(l10n_it_edi_intermediary_id.display_name, "INTERMEDIARIO SRL")
