# Copyright 2019 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import datetime

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestIntrastat(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.partner01 = cls.env.ref("base.res_partner_1")
        cls.product01 = cls.env.ref("product.product_product_10")
        cls.account_account_model = cls.env["account.account"]
        cls.fp_model = cls.env["account.fiscal.position"]
        cls.partner_model = cls.env["res.partner"]
        cls.res_currency_rate_model = cls.env["res.currency.rate"]

        cls.account_account_receivable = cls.account_account_model.create(
            {
                "code": "1",
                "name": "Debtors - (test)",
                "reconcile": True,
                "user_type_id": cls.env.ref("account.data_account_type_receivable").id,
            }
        )

        cls.account_account_payable = cls.account_account_model.create(
            {
                "code": "2",
                "name": "Creditors - (test)",
                "reconcile": True,
                "user_type_id": cls.env.ref("account.data_account_type_payable").id,
            }
        )

        cls.partner01.property_account_receivable_id = cls.account_account_receivable
        cls.partner01.property_account_payable_id = cls.account_account_payable

        partner_not_euro_country = cls.env["res.country"].search(
            [("name", "ilike", "poland")], limit=1
        )
        partner_not_euro_country.currency_id.active = True
        cls.partner_not_euro = cls.partner_model.create(
            {
                "name": "AMAZON EU s.a.r.l. (Poland)",
                "vat": "PL5262907815",
                "street": "Ul. Rondo Daszynskiego 1",
                "city": "Warsav",
                "zip": "00000",
                "country_id": partner_not_euro_country.id,
            }
        )

        cls.res_currency_rate_model.create(
            {
                "currency_id": partner_not_euro_country.currency_id.id,
                "name": fields.Date.to_string(fields.Date.today()),
                "rate": "1.0",
            }
        )

        # Demo tax is in another company than current user's company.
        # We can't change this tax's company because
        # it is the default sale tax for the company
        # and it has already been used in other invoices.
        cls.tax22 = (
            cls.env.ref("l10n_it_intrastat.tax_22")
            .sudo()
            .copy(default={"company_id": cls.env.company.id})
        )

    def test_invoice_totals(self):
        invoice = self.init_invoice(
            "out_invoice",
            partner=self.partner01,
            products=self.product01,
            taxes=self.tax22,
        )
        invoice.intrastat = True

        # Compute intrastat lines
        invoice.compute_intrastat_lines()
        self.assertEqual(invoice.intrastat, True)
        # Amount Control
        total_intrastat_amount = sum(
            line.amount_currency for line in invoice.intrastat_line_ids
        )
        self.assertEqual(total_intrastat_amount, invoice.amount_untaxed)

    def test_invoice_fiscal_postion(self):
        self.partner01.property_account_position_id = self.fp_model.create(
            {
                "name": "F.P subjected to intrastat",
                "intrastat": True,
            }
        )
        invoice = self.init_invoice(
            "out_invoice",
            partner=self.partner01,
            products=self.product01,
            taxes=self.tax22,
        )
        # Compute intrastat lines
        invoice.action_post()
        invoice.compute_intrastat_lines()
        self.assertEqual(invoice.intrastat, True)

    def test_currency_not_active_raise_exception(self):
        self.partner_not_euro.country_id.currency_id.active = False
        with self.assertRaises(UserError):
            invoice = self.invoice_model.create(
                {
                    "partner_id": self.partner_not_euro.id,
                    "journal_id": self.sales_journal.id,
                    "account_id": self.account_account_receivable.id,
                    "date_invoice": fields.Date.today(),
                    "intrastat": True,
                    "invoice_line_ids": [
                        (
                            0,
                            0,
                            {
                                "name": "service",
                                "product_id": self.product01.id,
                                "account_id": self.account_account_receivable.id,
                                "quantity": 1,
                                "price_unit": 100,
                                "invoice_line_tax_ids": [(6, 0, {self.tax22.id})],
                            },
                        )
                    ],
                }
            )

        invoice.compute_taxes()
        invoice.action_invoice_open()

        # Compute intrastat lines
        invoice.compute_intrastat_lines()

    def test_no_currency_rate_raise_exception(self):
        currency_rate_date = fields.Date.today() - datetime.timedelta(days=1)
        with self.assertRaises(UserError):
            invoice = self.invoice_model.create(
                {
                    "partner_id": self.partner_not_euro.id,
                    "journal_id": self.sales_journal.id,
                    "account_id": self.account_account_receivable.id,
                    "date_invoice": currency_rate_date,
                    "intrastat": True,
                    "invoice_line_ids": [
                        (
                            0,
                            0,
                            {
                                "name": "service",
                                "product_id": self.product01.id,
                                "account_id": self.account_account_receivable.id,
                                "quantity": 1,
                                "price_unit": 100,
                                "invoice_line_tax_ids": [(6, 0, {self.tax22.id})],
                            },
                        )
                    ],
                }
            )

            invoice.compute_taxes()
            invoice.action_invoice_open()

            # Compute intrastat lines
            invoice.compute_intrastat_lines()

    def test_invoice_totals_partner_no_euro(self):
        invoice = self.invoice_model.create(
            {
                "partner_id": self.partner_not_euro.id,
                "journal_id": self.sales_journal.id,
                "account_id": self.account_account_receivable.id,
                "date_invoice": fields.Date.today(),
                "intrastat": True,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "service",
                            "product_id": self.product01.id,
                            "account_id": self.account_account_receivable.id,
                            "quantity": 1,
                            "price_unit": 100,
                            "invoice_line_tax_ids": [(6, 0, {self.tax22.id})],
                        },
                    )
                ],
            }
        )

        invoice.compute_taxes()
        invoice.action_invoice_open()

        # Compute intrastat lines
        invoice.compute_intrastat_lines()
        self.assertEqual(invoice.intrastat, True)
        # Amount Control
        total_intrastat_amount = sum(
            line.amount_currency for line in invoice.intrastat_line_ids
        )
        invoice_amount_currency = invoice.currency_id._convert(
            invoice.amount_untaxed,
            self.partner_not_euro.country_id.currency_id,
            invoice.company_id,
            invoice.date_invoice or fields.Date.today(),
        )
        self.assertEqual(total_intrastat_amount, invoice_amount_currency)
