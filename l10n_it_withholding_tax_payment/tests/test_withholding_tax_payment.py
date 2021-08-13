#  Copyright 2021 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import Form

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


class TestWithholdingTaxPayment(AccountTestInvoicingCommon):
    @classmethod
    def setup_withholding_tax(cls, company_data):
        return cls.env["withholding.tax"].create(
            {
                "name": "Test withholding tax",
                "code": "TWHT",
                "company_id": company_data["company"].id,
                "account_receivable_id": company_data["default_account_receivable"].id,
                "account_payable_id": company_data["default_account_payable"].id,
                "journal_id": company_data["default_journal_misc"].id,
                "payment_term": cls.pay_terms_a.id,
                "rate_ids": [
                    (
                        0,
                        0,
                        {
                            "tax": 20,
                            "base": 1,
                        },
                    )
                ],
            }
        )

    @classmethod
    def setup_withholding_data(cls, company_data):
        """
        Create an invoice with a withholding tax for current company.
        """
        cls.set_allowed_companies(company_data["company"])
        wh_tax = cls.setup_withholding_tax(company_data)
        invoice = cls.init_invoice("in_invoice", amounts=[100])
        invoice_form = Form(invoice)
        with invoice_form.invoice_line_ids.edit(0) as line_form:
            line_form.invoice_line_tax_wt_ids.clear()
            line_form.invoice_line_tax_wt_ids.add(wh_tax)
        invoice = invoice_form.save()
        return invoice

    @classmethod
    def set_allowed_companies(cls, company):
        """
        Set company for current user.
        Note that user.company_id would not be the current company
        but only the default company for the user.
        """
        context = {"allowed_company_ids": company.ids}
        if "allowed_company_ids" in cls.env.context:
            cls.env.context.pop("allowed_company_ids")
        cls.env.context = dict(**cls.env.context, **context)

    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.invoice_1 = cls.setup_withholding_data(cls.company_data)
        cls.invoice_2 = cls.setup_withholding_data(cls.company_data_2)

    def generate_withholding_tax_payment(self, invoice):
        """
        Generate payment for withholding tax included in `invoice`.
        """
        self.set_allowed_companies(invoice.company_id)

        # Pay invoice
        invoice.action_post()
        payment_wizard = (
            self.env["account.payment.register"]
            .with_context(
                active_model=invoice._name,
                active_ids=invoice.ids,
            )
            .create({})
        )
        action_payment = payment_wizard.action_create_payments()
        self.assertTrue(invoice.payment_state, "partial")

        # Pay withholding tax
        payment = self.env[action_payment["res_model"]].browse(action_payment["res_id"])
        wh_tax_move = self.env["withholding.tax.move"].search(
            [("account_move_id", "=", payment.move_id.id)]
        )
        wh_tax_payment_wizard = (
            self.env["wizard.wt.move.payment.create"]
            .with_context(active_model=wh_tax_move._name, active_ids=wh_tax_move.ids)
            .create({})
        )
        wh_tax_payment_action = wh_tax_payment_wizard.generate()
        withholding_tax_payment = self.env[wh_tax_payment_action["res_model"]].browse(
            wh_tax_payment_action["res_id"]
        )
        return withholding_tax_payment

    def test_withholding_tax_payment_multi_company_security(self):
        """
        Check that withholding tax payments can be generated
        in multi-company environment.
        """
        withholding_tax_payment_1 = self.generate_withholding_tax_payment(
            self.invoice_1
        )
        self.assertTrue(withholding_tax_payment_1)

        # Generate payment in second company
        withholding_tax_payment_2 = self.generate_withholding_tax_payment(
            self.invoice_2
        )
        self.assertTrue(withholding_tax_payment_2)
