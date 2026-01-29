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
        cls.partner01 = cls.env["res.partner"].create(
            {
                "name": "Wood Corner",
                "is_company": True,
                "street": "1839 Arbor Way",
                "city": "Turlock",
                "state_id": cls.env.ref("base.state_us_5").id,
                "zip": "95380",
                "email": "wood.corner26@example.com",
                "phone": "(623)-853-7197",
                "vat": "US12345672",
            }
        )

        cls.intrastat_01012100 = cls.env["report.intrastat.code"].create(
            {
                "name": "Pure-bred breeding horses",
                "type": "good",
            }
        )
        cls.product01 = cls.env["product.product"].create(
            {
                "name": "Cabinet with Doors",
                "type": "consu",
                "list_price": 140.0,
                "weight": 0.01,
                "default_code": "E-COM11",
                "intrastat_type": "good",
                "intrastat_code_id": cls.intrastat_01012100.id,
            }
        )
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

    def test_invoice_totals(self):
        invoice = self.init_invoice(
            "out_invoice",
            partner=self.partner01,
            products=self.product01,
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
        self.partner01.property_account_position_id = self.fp_model.create(
            {
                "name": "F.P subjected to intrastat",
                "l10n_it_oca_intrastat": True,
            }
        )
        invoice = self.init_invoice(
            "out_invoice",
            partner=self.partner01,
            products=self.product01,
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

        attribute = self.env["product.attribute"].create(
            {
                "name": "Test attribute",
                "value_ids": [
                    Command.create({"name": "Test value 1"}),
                    Command.create({"name": "Test value 2"}),
                ],
            }
        )
        template = self.env["product.template"].create(
            {
                "name": "Test Product",
                "type": "consu",
                "list_price": 140.0,
                "weight": 0.0,
                "default_code": "E-COM11",
                "intrastat_type": "good",
                "intrastat_code_id": self.intrastat_01012100.id,
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": attribute.id,
                            "value_ids": [Command.set(attribute.value_ids.ids)],
                        }
                    )
                ],
            }
        )

        self.assertEqual(len(template.product_variant_ids), 2)
        variant = next(iter(template.product_variant_ids), template.product_variant_ids)
        variant.weight = variant_weight
        # pre-condition
        self.assertFalse(template.weight)
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
