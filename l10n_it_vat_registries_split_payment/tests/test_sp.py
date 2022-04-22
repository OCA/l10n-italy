from odoo import fields
from odoo.tests import Form, tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestSP(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.account_model = cls.env["account.account"]
        cls.tax_model = cls.env["account.tax"]
        cls.invoice_model = cls.env["account.move"]
        cls.inv_line_model = cls.env["account.move.line"]
        cls.fp_model = cls.env["account.fiscal.position"]
        cls.tax_received = cls.account_model.search(
            [("name", "=", "Tax Received"), ("company_id", "=", cls.env.company.id)]
        )
        cls.tax22sp = cls.tax_model.create(
            {
                "name": "22% SP",
                "amount": 22,
                "invoice_repartition_line_ids": [
                    (5, 0, 0),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "base",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "tax",
                            "account_id": cls.tax_received.id,
                        },
                    ),
                ],
                "refund_repartition_line_ids": [
                    (5, 0, 0),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "base",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "tax",
                            "account_id": cls.tax_received.id,
                        },
                    ),
                ],
            }
        )
        cls.tax22 = cls.tax_model.create(
            {
                "name": "22%",
                "amount": 22,
                "invoice_repartition_line_ids": [
                    (5, 0, 0),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "base",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "tax",
                            "account_id": cls.tax_received.id,
                        },
                    ),
                ],
                "refund_repartition_line_ids": [
                    (5, 0, 0),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "base",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "tax",
                            "account_id": cls.tax_received.id,
                        },
                    ),
                ],
            }
        )
        cls.sp_fp = cls.fp_model.create(
            {
                "name": "Split payment",
                "split_payment": True,
                "tax_ids": [
                    (
                        0,
                        0,
                        {"tax_src_id": cls.tax22.id, "tax_dest_id": cls.tax22sp.id},
                    )
                ],
            }
        )
        cls.company = cls.env.company
        cls.company.sp_account_id = cls.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    cls.env.ref("account.data_account_type_current_assets").id,
                )
            ],
            limit=1,
        )
        cls.a_sale = cls.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    cls.env.ref("account.data_account_type_revenue").id,
                )
            ],
            limit=1,
        )
        cls.invoice_date = fields.Date.today()

    def test_invoice(self):
        partner = self.env.ref("base.res_partner_3")

        for tax in (self.tax22, self.tax22sp):
            invoice = self.init_invoice(
                "out_invoice",
                partner=partner,
                invoice_date=self.invoice_date,
                amounts=[100],
                taxes=tax,
            )
            invoice_form = Form(invoice)
            invoice_form.fiscal_position_id = self.sp_fp
            invoice = invoice_form.save()
            invoice.action_post()

        data = {
            "from_date": self.invoice_date,
            "to_date": self.invoice_date,
        }
        totals_standard_sp = self.tax22sp._compute_totals_tax(data)
        totals_standard = self.tax22._compute_totals_tax(data)

        self.assertEqual(totals_standard_sp, ("22% SP", 100.0, 22.0, 22.0, 0))
        self.assertEqual(totals_standard, ("22%", 100.0, 22.0, 22.0, 0))

        report_vat_registry = self.env[
            "report.l10n_it_vat_registries.report_registro_iva"
        ]
        totals_registry_sp = report_vat_registry._compute_totals_tax(self.tax22sp, data)
        totals_registry = report_vat_registry._compute_totals_tax(self.tax22, data)

        self.assertEqual(totals_registry_sp, ("22% SP", 100.0, 22.0, 0.0, 0))
        self.assertEqual(totals_registry, ("22%", 100.0, 22.0, 22.0, 0))
