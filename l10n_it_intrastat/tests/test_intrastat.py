# Copyright 2019 Simone Rubino - Agile Business Group
# Copyright 2024 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from unittest import mock

from odoo import Command
from odoo.fields import first
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

        cls.account_account_receivable = cls.account_account_model.create(
            {
                "code": "1",
                "name": "Debtors - (test)",
                "reconcile": True,
                "account_type": "asset_receivable",
            }
        )

        cls.account_account_payable = cls.account_account_model.create(
            {
                "code": "2",
                "name": "Creditors - (test)",
                "reconcile": True,
                "account_type": "liability_payable",
            }
        )

        cls.partner01.property_account_receivable_id = cls.account_account_receivable
        cls.partner01.property_account_payable_id = cls.account_account_payable

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

    def test_propagate_action_post_result(self):
        """The result of posting an invoice is propagated."""
        expected_post_result = "Test post result"
        from odoo.addons.account.models.account_move import AccountMove

        with mock.patch.object(AccountMove, "action_post") as core_post_method:
            core_post_method.return_value = expected_post_result
            invoice = self.init_invoice("out_invoice")
            post_result = invoice.action_post()
        self.assertEqual(post_result, expected_post_result)

    def test_line_variant_weight(self):
        """Weight from variants is propagated to the intrastat lines."""
        # Arrange
        variant_weight = 100
        product = self.product01
        product.weight = 0

        attribute = self.env["product.attribute"].create(
            {
                "name": "Test attribute",
                "value_ids": [
                    Command.create(
                        {
                            "name": "Test value 1",
                        }
                    ),
                    Command.create(
                        {
                            "name": "Test value 2",
                        }
                    ),
                ],
            }
        )
        product.attribute_line_ids = [
            Command.create(
                {
                    "attribute_id": attribute.id,
                    "value_ids": [
                        Command.set(attribute.value_ids.ids),
                    ],
                }
            )
        ]
        variant = first(product.product_variant_ids)
        variant.weight = variant_weight
        # pre-condition
        self.assertFalse(product.weight)
        self.assertEqual(variant.weight, variant_weight)

        # Act
        invoice = self.init_invoice(
            "out_invoice",
            products=variant,
        )
        invoice.intrastat = True
        invoice.action_post()

        # Assert
        self.assertEqual(invoice.intrastat_line_ids.weight_kg, variant_weight)
