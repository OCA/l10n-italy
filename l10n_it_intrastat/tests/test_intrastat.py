# Copyright 2019 Simone Rubino - Agile Business Group
# Copyright 2024 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from unittest import mock

from odoo import Command
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestIntrastat(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.fp_model = cls.env["account.fiscal.position"]
        # Use existing intrastat code from module data
        cls.intrastat_code = cls.env.ref(
            "l10n_it_intrastat.intrastat_category_2014_01012100"
        )
        # Create product with intrastat configuration
        cls.intrastat_product = cls.env["product.template"].create(
            {
                "name": "Intrastat Test Product",
                "type": "consu",
                "list_price": 1000.0,
                "weight": 0,
                "intrastat_type": "good",
                "intrastat_code_id": cls.intrastat_code.id,
            }
        )

    def test_invoice_totals(self):
        invoice = self.init_invoice(
            "out_invoice",
            partner=self.partner_a,
            products=self.intrastat_product.product_variant_ids[:1],
            taxes=self.tax_sale_a,
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

    def test_invoice_fiscal_position(self):
        self.partner_a.property_account_position_id = self.fp_model.create(
            {
                "name": "F.P subjected to intrastat",
                "l10n_it_oca_intrastat": True,
            }
        )
        invoice = self.init_invoice(
            "out_invoice",
            partner=self.partner_a,
            products=self.intrastat_product.product_variant_ids[:1],
            taxes=self.tax_sale_a,
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
        product = self.intrastat_product
        # Ensure product has no weight initially
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
        variant = product.product_variant_ids[:1]
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
