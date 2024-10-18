#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from odoo.exceptions import UserError
from odoo.tests import Form, tagged

from odoo.addons.l10n_it_fatturapa_out.tests.fatturapa_common import (
    FatturaPACommon,
)


@tagged("post_install", "-at_install")
class TestFatturaPAOUTWelfare(FatturaPACommon):
    def _get_welfare_amount(self, welfare, amount):
        """
        Return a Welfare Amount of type `welfare` and amount `amount`.
        """
        welfare_amount_model = self.env["welfare.fund.type.amount"]
        welfare_amount_form = Form(welfare_amount_model)
        welfare_amount_form.welfare_fund_type_id = welfare
        welfare_amount_form.amount = amount
        return welfare_amount_form.save()

    def _get_payable_account(self):
        """
        Return an account of Type Payable.
        """
        account_model = self.env["account.account"]
        payable_account_form = Form(account_model)
        payable_account_form.name = "Withholding Credit"
        payable_account_form.code = "WTPAY"
        payable_account_form.account_type = "liability_payable"
        payable_account = payable_account_form.save()
        return payable_account

    def _get_withholding_tax(self, payable_account, receivable_account):
        """
        Return a 20% Withholding Tax.
        """
        withholding_tax_model = self.env["withholding.tax"]
        withholding_tax_form = Form(withholding_tax_model)
        withholding_tax_form.name = "Test WT"
        withholding_tax_form.code = "TWT"
        withholding_tax_form.account_receivable_id = receivable_account
        withholding_tax_form.account_payable_id = payable_account
        withholding_tax_form.payment_reason_id = self.env.ref(
            "l10n_it_payment_reason.a"
        )
        withholding_tax_form.payment_term = self.env.ref(
            "account.account_payment_term_immediate"
        )
        with withholding_tax_form.rate_ids.new() as rate:
            rate.tax = 20
            rate.base = 1
        withholding_tax = withholding_tax_form.save()
        return withholding_tax

    def _get_invoice(self):
        """
        Return an invoice having 3 lines:
        - subtotal 100,
        - subtotal 100, with 10% Welfare and 20% Withholding Tax
        - subtotal 100, with 10% Welfare and 20% on another Welfare
        """
        # Cancel other open invoices to avoid conflict on date or sequence
        open_invoices = self.invoice_model.search(
            [
                ("state", "=", "open"),
            ],
        )
        open_invoices.button_cancel()

        invoice = self.invoice_model.create(
            {
                "invoice_date": "2024-01-01",
                "partner_id": self.res_partner_fatturapa_0.id,
                "journal_id": self.sales_journal.id,
                "invoice_payment_term_id": self.account_payment_term.id,
                "user_id": self.user_demo.id,
                "move_type": "out_invoice",
                "currency_id": self.EUR.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_product_10.id,
                            "price_unit": 100,
                            "tax_ids": [(6, 0, [self.tax_22.id])],
                            "welfare_fund_type_amount_ids": [(5, 0, 0)],
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_product_10.id,
                            "price_unit": 100,
                            "tax_ids": [(6, 0, [self.tax_22.id])],
                            "invoice_line_tax_wt_ids": [
                                (6, 0, [self.withholding_tax.id])
                            ],
                            "welfare_fund_type_amount_ids": [
                                (6, 0, [self.welfare_amount_INPS_10.id])
                            ],
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_product_10.id,
                            "price_unit": 100,
                            "tax_ids": [(6, 0, [self.tax_22.id])],
                            "invoice_line_tax_wt_ids": [
                                (6, 0, [self.withholding_tax.id])
                            ],
                            "welfare_fund_type_amount_ids": [
                                (
                                    6,
                                    0,
                                    [
                                        self.welfare_amount_ENPAM_20.id,
                                        self.welfare_amount_INPS_10.id,
                                    ],
                                )
                            ],
                        },
                    ),
                ],
            }
        )
        return invoice

    def setUp(self):
        super().setUp()
        self.company = self.env.company = self.sales_journal.company_id

        # XXX - a company named "YourCompany" alread exists
        # we move it out of the way but we should do better here
        self.env.company.sudo().search([("name", "=", "YourCompany")]).write(
            {"name": "YourCompany_"}
        )
        self.env.company.name = "YourCompany"
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
        self.welfare_amount_INPS_10 = self._get_welfare_amount(
            self.env.ref("l10n_it_fatturapa.21"),
            10,
        )

        self.welfare_amount_ENPAM_20 = self._get_welfare_amount(
            self.env.ref("l10n_it_fatturapa.8"),
            20,
        )

        self.withholding_tax = self._get_withholding_tax(
            self._get_payable_account(),
            self.a_recv,
        )

    def test_export_welfare_withholding(self):
        """
        Check that an invoice having Welfare Amounts and Withholding Taxes
        is correctly converted to an Electronic Invoice.
        """
        invoice = self._get_invoice()

        # Check that Welfare Lines have to be generated
        # before validating the invoice
        with self.assertRaises(UserError) as ue:
            invoice.action_post()
        exc_message = ue.exception.args[0]
        self.assertIn("regenerate Welfare Lines", exc_message)
        self.assertIn(invoice.display_name, exc_message)

        # Export the Electronic Invoice
        invoice._onchange_invoice_line_wt_ids()
        invoice.button_regenerate_welfare_lines()
        invoice.action_post()
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_random.xml")

        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(
            xml_content,
            "IT06363391001_random.xml",
            module_name="l10n_it_fatturapa_out_welfare",
        )
