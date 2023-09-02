#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.mail.tests.common import MailCommon


class TestFatturaPAAttachmentIn(MailCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.attachment_model = cls.env["fatturapa.attachment.in"]
        cls.env.company.sudo().search([("name", "=", "YourCompany")]).write(
            {"name": "YourCompany_"}
        )
        cls.env.company.name = "YourCompany"
        cls.env.company.vat = "IT06363391001"
        cls.env.company.fatturapa_art73 = True
        cls.env.company.partner_id.street = "Via Milano, 1"
        cls.env.company.partner_id.city = "Roma"
        cls.env.company.partner_id.state_id = cls.env.ref("base.state_us_2").id
        cls.env.company.partner_id.zip = "00100"
        cls.env.company.partner_id.phone = "06543534343"
        cls.env.company.email = "info@yourcompany.example.com"
        cls.env.company.partner_id.country_id = cls.env.ref("base.it").id
        cls.env.company.fatturapa_fiscal_position_id = cls.env.ref(
            "l10n_it_fatturapa.fatturapa_RF01"
        ).id
        cls.env.e_invoice_user_id = cls.env.ref("base.user_root")

    def test_receive_fe(self):

        # check that assigned company is "YourCompany"
        company_id = self.env["res.company"].search([("name", "=", "YourCompany")])
        self.assertEqual(self.env.company.id, company_id.id)

        # check "einvoice_user_id"
        einvoice_user_id = self.env.company.e_invoice_user_id
        self.assertEqual(einvoice_user_id.id, self.env.ref("base.user_root").id)
        self.assertEqual(einvoice_user_id.id, company_id.e_invoice_user_id.id)

        if einvoice_user_id:
            self.attachment_model = self.attachment_model.with_user(einvoice_user_id.id)

    def test_prepare_attachment_in_values(self):

        # check that assigned company is "YourCompany"
        company_id = self.env["res.company"].search([("name", "=", "YourCompany")])
        self.assertEqual(self.env.company.id, company_id.id)

        # check "einvoice_user_id"
        einvoice_user_id = self.env.company.e_invoice_user_id
        self.assertEqual(einvoice_user_id.id, self.env.ref("base.user_root").id)
        self.assertEqual(einvoice_user_id.id, company_id.e_invoice_user_id.id)

        if einvoice_user_id:
            self.attachment_model = self.attachment_model.with_user(einvoice_user_id.id)
