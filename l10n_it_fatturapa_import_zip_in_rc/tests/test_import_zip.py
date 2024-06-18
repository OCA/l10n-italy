#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.l10n_it_fatturapa_in.tests.fatturapa_common import FatturapaCommon


class TestImportZIP(FatturapaCommon):
    def getFile(self, filename, module_name=None):
        if module_name is None:
            module_name = "l10n_it_fatturapa_import_zip_in_rc"
        return super().getFile(
            filename,
            module_name=module_name,
        )

    @classmethod
    def _setup_import_zip_in_rc_taxes(cls):
        cls.sale_tax = cls.env["account.tax"].create(
            {
                "name": "Tax 22% Sale",
                "type_tax_use": "sale",
                "amount": 22,
            }
        )
        cls.sale_n6_1_tax = cls.env["account.tax"].create(
            {
                "name": "Tax 22% Sale N6.1",
                "type_tax_use": "sale",
                "amount": 0,
                "kind_id": cls.n6_1_tax_kind.id,
            }
        )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.company.vat = "IT02780790107"
        cls.n6_1_tax_kind = cls.env.ref("l10n_it_account_tax_kind.n6_1")
        cls._setup_import_zip_in_rc_taxes()

    def test_reverse_charge_out(self):
        """Import a reverse charge electronic invoice created by current company,
        it is not imported as reverse charge and it is a customer invoice.
        """
        # Arrange
        file_name = "IT01234567890_FPR04.zip"
        file_path, file_content = self.getFile(file_name)
        wizard_attachment_import = self.env["fatturapa.attachment.import.zip"].create(
            {
                "name": file_name,
                "datas": file_content,
            }
        )
        # Act
        wizard_attachment_import.action_import()

        # Assert
        attachment_out = wizard_attachment_import.attachment_out_ids
        self.assertEqual(len(attachment_out), 1)
        self.assertFalse(wizard_attachment_import.invoice_in_ids)

        invoice = attachment_out.out_invoice_ids
        self.assertEqual(invoice.move_type, "out_invoice")
        self.assertRecordValues(
            invoice.invoice_line_ids,
            [
                {
                    "name": "LA DESCRIZIONE",
                    "tax_ids": self.sale_tax.ids,
                    "rc": False,
                },
                {
                    "name": "BANCALI",
                    "tax_ids": self.sale_n6_1_tax.ids,
                    "rc": False,
                },
            ],
        )
