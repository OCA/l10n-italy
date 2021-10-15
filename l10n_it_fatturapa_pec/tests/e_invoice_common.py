# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.l10n_it_fatturapa_out.tests.fatturapa_common import FatturaPACommon


class EInvoiceCommon(FatturaPACommon):
    def setUp(self):
        super(EInvoiceCommon, self).setUp()
        self.account_model = self.env["account.account"]
        self.invoice_model = self.env["account.move"]
        self.wizard_model = self.env["wizard.export.fatturapa"]
        self.tax_model = self.env["account.tax"]

        self.env.company.vat = "IT06363391001"
        self.env.company.fatturapa_art73 = True
        self.env.company.partner_id.street = "Via Milano, 1"
        self.env.company.partner_id.city = "Roma"
        self.env.company.partner_id.state_id = self.env.ref("base.state_us_2").id
        self.env.company.partner_id.zip = "00100"
        self.env.company.partner_id.phone = "06543534343"
        self.env.company.email = "info@yourcompany.example.com"
        self.env.company.partner_id.country_id = self.env.ref("base.it").id
        self.env.company.fatturapa_fiscal_position_id = self.env.ref(
            "l10n_it_fatturapa.fatturapa_RF01"
        ).id

        self.account_receivable_id = self.account_model.create(
            dict(
                code="REC",
                name="Receivable",
                user_type_id=self.ref("account.data_account_type_receivable"),
                reconcile=True,
            )
        )
        self.account_income_id = self.account_model.create(
            dict(
                code="INC",
                name="Income",
                user_type_id=self.ref("account.data_account_type_revenue"),
                reconcile=True,
            )
        )
        self.partner = self.env.ref("l10n_it_fatturapa.res_partner_fatturapa_2")
        self.product = self.env.ref("product.product_product_5")
        self.env.company.sdi_channel_id = self.env.ref(
            "l10n_it_sdi_channel.sdi_channel_pec"
        )
        self.env.company.sdi_channel_id.pec_server_id = self.env[
            "ir.mail_server"
        ].create(
            {
                "name": "dummy",
                "smtp_host": "smtp_host",
                "email_from_for_fatturaPA": "dummy@fatturapa.it",
            }
        )

    def _create_invoice(self):
        tax = self.tax_model.create(
            {
                "name": "Tax 22.0%",
                "amount": 22,
                "amount_type": "percent",
                "type_tax_use": "sale",
            }
        )
        invoice_line_data = {
            "product_id": self.product.id,
            "quantity": 1,
            "price_unit": 1,
            "account_id": self.account_income_id.id,
            "name": self.product.name,
            "tax_ids": [(6, 0, [tax.id])],
        }
        return self.invoice_model.create(
            dict(
                name="Test Invoice",
                invoice_line_ids=[(0, 0, invoice_line_data)],
                partner_id=self.partner.id,
                move_type="out_invoice",
            )
        )

    def _get_export_wizard(self, invoice):
        wizard = self.wizard_model.create({})
        return wizard.with_context({"active_ids": [invoice.id]})

    def _create_e_invoice(self):
        invoice = self._create_invoice()
        invoice.action_post()

        wizard = self._get_export_wizard(invoice)
        action = wizard.exportFatturaPA()

        return self.env[action["res_model"]].browse(action["res_id"])

    def _create_fetchmail_pec_server(self):
        return self.env["fetchmail.server"].create(
            {
                "name": "Test PEC server",
                "server_type": "pop",
                "is_fatturapa_pec": True,
                "server": "dummy",
                "port": 110,
                "user": "dummy",
                "password": "secret",
                "state": "done",
                "e_inv_notify_partner_ids": [
                    (6, 0, [self.env.ref("base.user_admin").partner_id.id])
                ],
            }
        )
