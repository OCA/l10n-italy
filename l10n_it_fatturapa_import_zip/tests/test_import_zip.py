#  Copyright 2023 Simone Rubino - TAKOBI
#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date

from odoo.addons.l10n_it_fatturapa_in.tests.fatturapa_common import FatturapaCommon


class TestImportZIP(FatturapaCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.company.vat = "IT06363391001"

    def setUp(self):
        super().setUp()
        self.attachment_import_model = self.env["fatturapa.attachment.import.zip"]
        self.cleanPartners()
        self.create_wt()
        self.create_wt_enasarco_157_r()
        self.create_wt_enasarco_85_r()
        self.create_wt_enasarco_115_a()
        self.create_wt_115_r()
        self.create_wt_23_20()
        self.create_wt_26_20q()
        self.create_wt_26_40q()
        self.create_wt_27_20q()
        self.create_wt_4q()

        AED = self.env.ref("base.AED")
        AED.active = True

    def cleanPartners(self):
        # VAT number used in tests, assigned to other partners by demo data, probably
        main_company = self.env.company
        partners = self.env["res.partner"].search([("vat", "=", "IT06363391001")])
        for partner in partners:
            if partner.id != main_company.partner_id.id:
                partner.vat = ""

    def getFile(self, filename, module_name="l10n_it_fatturapa_import_zip"):
        return super().getFile(
            filename,
            module_name=module_name,
        )

    def test_import_zip(self):
        wizard_attachment_import = self.attachment_import_model.create(
            {
                "name": "xml_import.zip",
                "datas": self.getFile("xml_import.zip")[1],
            }
        )
        wizard_attachment_import.action_import()
        attachments_out = wizard_attachment_import.attachment_out_ids
        attachments_in = wizard_attachment_import.invoice_in_ids
        self.assertEqual(len(attachments_out), 6)
        self.assertEqual(len(attachments_in), 37)

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

        for attachment in attachments_out:
            expected_invoices_values = check_invoices_values.get(attachment.name)
            if expected_invoices_values is not None:
                invoices = attachment.out_invoice_ids
                for invoice, expected_values in zip(
                    invoices,
                    expected_invoices_values,
                    strict=True,
                ):
                    for field, expected_value in expected_values.items():
                        self.assertEqual(
                            getattr(invoice, field),
                            expected_value,
                            f"Field {field} of invoice {invoice.display_name} "
                            f"does not match",
                        )

    def test_access_other_user_zip(self):
        """A user can see the zip files imported by other users."""
        # Arrange
        user = self.env.user
        other_user = user.copy()
        # pre-condition
        self.assertNotEqual(user, other_user)

        # Act
        wizard_attachment_import = self.attachment_import_model.with_user(
            other_user
        ).create(
            {
                "name": "Test other user XML import",
                "datas": self.getFile("xml_import.zip")[1],
            }
        )

        # Assert
        self.assertTrue(
            wizard_attachment_import.ir_attachment_id.with_user(user).read()
        )
