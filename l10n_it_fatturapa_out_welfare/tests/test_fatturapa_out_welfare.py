#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from odoo.exceptions import UserError
from odoo.tests import Form

from odoo.addons.l10n_it_fatturapa_out.tests.fatturapa_common import (
    FatturaPACommon,
)


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
        payable_account_form.user_type_id = self.env.ref(
            "account.data_account_type_payable"
        )
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
        withholding_tax_form.causale_pagamento_id = self.env.ref(
            "l10n_it_causali_pagamento.a"
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
        journals = open_invoices.mapped("journal_id")
        journals.update(
            {
                "update_posted": True,
            }
        )
        open_invoices.action_cancel()

        date_invoice = "2023-01-01"
        self.set_sequences(1, date_invoice)
        # Explicitly request the customer invoice form view,
        # otherwise the supplier form view is automatically picked up
        invoice_form = Form(
            self.invoice_model,
            "account.invoice_form",
        )
        invoice_form.partner_id = self.res_partner_fatturapa_0
        invoice_form.date_invoice = date_invoice
        with invoice_form.invoice_line_ids.new() as invoice_line:
            invoice_line.product_id = self.product_product_10
            invoice_line.price_unit = 100
            invoice_line.invoice_line_tax_ids.clear()
            invoice_line.invoice_line_tax_ids.add(
                self.tax_22,
            )
            invoice_line.welfare_fund_type_amount_ids.clear()

        with invoice_form.invoice_line_ids.new() as invoice_line:
            invoice_line.product_id = self.product_product_10
            invoice_line.price_unit = 100
            invoice_line.invoice_line_tax_ids.clear()
            invoice_line.invoice_line_tax_ids.add(
                self.tax_22,
            )
            invoice_line.welfare_fund_type_amount_ids.clear()
            invoice_line.welfare_fund_type_amount_ids.add(
                self.welfare_amount_INPS_10,
            )
            invoice_line.invoice_line_tax_wt_ids.clear()
            invoice_line.invoice_line_tax_wt_ids.add(
                self.withholding_tax,
            )

        with invoice_form.invoice_line_ids.new() as invoice_line:
            invoice_line.product_id = self.product_product_10
            invoice_line.price_unit = 100
            invoice_line.invoice_line_tax_ids.clear()
            invoice_line.invoice_line_tax_ids.add(
                self.tax_22,
            )
            invoice_line.welfare_fund_type_amount_ids.clear()
            invoice_line.welfare_fund_type_amount_ids.add(
                self.welfare_amount_ENPAM_20,
            )
            invoice_line.welfare_fund_type_amount_ids.add(
                self.welfare_amount_INPS_10,
            )
        invoice = invoice_form.save()
        return invoice

    def setUp(self):
        super().setUp()
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
            invoice.action_invoice_open()
        exc_message = ue.exception.args[0]
        self.assertIn("regenerate Welfare Lines", exc_message)
        self.assertIn(invoice.display_name, exc_message)

        # Export the Electronic Invoice
        invoice.button_regenerate_welfare_lines()
        invoice.action_invoice_open()
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_random.xml")

        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(
            xml_content,
            "IT06363391001_random.xml",
            module_name="l10n_it_fatturapa_out_welfare",
        )
