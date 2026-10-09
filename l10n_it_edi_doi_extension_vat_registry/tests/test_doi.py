# Copyright 2026 Simone Rubino
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from dateutil.relativedelta import relativedelta

from odoo import exceptions, fields, tests

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tests.tagged("-at_install", "post_install")
class TestDoiIssuedFromCompany(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.registry_excluded_tax, cls.registry_included_tax = cls.env[
            "account.tax"
        ].create(
            [
                {
                    "name": "Test Excluded Tax",
                    "amount": 0,
                    "exclude_from_registries": True,
                },
                {
                    "name": "Test Included Tax",
                    "amount": 0,
                    "exclude_from_registries": False,
                },
            ]
        )
        cls.customer, cls.supplier = cls.env["res.partner"].create(
            [
                {
                    "name": "Test customer",
                },
                {
                    "name": "Test supplier",
                },
            ]
        )

        cls.purchase_declaration = cls.env[
            "l10n_it_edi_doi.declaration_of_intent"
        ].create(
            {
                "partner_id": cls.supplier.id,
                "company_id": cls.env.company.id,
                "state": "active",
                "type": "in",
                "currency_id": cls.env.company.currency_id.id,
                "start_date": fields.Date.today(),
                "end_date": fields.Date.today() + relativedelta(months=2),
                "threshold": 5000,
                "protocol_number_part1": "20260000",
                "protocol_number_part2": "123456789",
            }
        )
        cls.env.company.l10n_it_edi_doi_bill_tax_id = cls.env["account.tax"].create(
            {
                "name": "Test DoI Purchase Tax",
                "type_tax_use": "purchase",
                "amount": 0,
            }
        )

        cls.sale_declaration = cls.env["l10n_it_edi_doi.declaration_of_intent"].create(
            {
                "partner_id": cls.customer.id,
                "company_id": cls.env.company.id,
                "state": "active",
                "type": "out",
                "currency_id": cls.env.company.currency_id.id,
                "start_date": fields.Date.today(),
                "end_date": fields.Date.today() + relativedelta(months=2),
                "threshold": 5000,
                "protocol_number_part1": "20260001",
                "protocol_number_part2": "123456789",
            }
        )
        cls.env.company.l10n_it_edi_doi_tax_id = cls.env["account.tax"].create(
            {
                "name": "Test DoI Sale Tax",
                "type_tax_use": "sale",
                "amount": 0,
            }
        )

    def _assert_invoice_validation(
        self,
        move_type,
        extra_taxes,
        expected_error_parts,
    ):
        """
        Create and post an Invoice, then check for expected errors.
        """
        # Arrange
        is_sale = move_type in self.env["account.move"].get_sale_types()
        doi_tax = (
            self.env.company.l10n_it_edi_doi_tax_id
            if is_sale
            else self.env.company.l10n_it_edi_doi_bill_tax_id
        )
        doi = self.sale_declaration if is_sale else self.purchase_declaration
        partner = self.customer if is_sale else self.supplier
        invoice = self.init_invoice(
            move_type,
            invoice_date=fields.Date.today(),
            partner=partner,
            amounts=[100],
            taxes=doi_tax + extra_taxes,
        )
        invoice.l10n_it_edi_doi_id = doi

        if expected_error_parts:
            # Act
            with self.assertRaises(exceptions.UserError) as ue:
                invoice.action_post()
            exc_message = ue.exception.args[0]

            # Assert
            for error_part in expected_error_parts:
                self.assertIn(error_part, exc_message)
        else:
            # Act
            invoice.action_post()

            # Assert
            self.assertEqual(invoice.state, "posted")

    def test_invoices_with_registry_tax(self):
        """Test adding excluded/included Taxes to Invoices."""
        excluded_tax = self.registry_excluded_tax
        included_tax = self.registry_included_tax

        included_error_parts = [
            "are not allowed",
            included_tax.name,
        ]
        move_types = ("in_invoice", "out_invoice")
        test_args_dict = {}
        test_args_dict.update(
            {
                f"Both Taxes for {move_type}": (
                    move_type,
                    excluded_tax + included_tax,
                    included_error_parts,
                )
                for move_type in move_types
            }
        )
        test_args_dict.update(
            {
                f"Only excluded Tax for {move_type}": (move_type, excluded_tax, None)
                for move_type in move_types
            }
        )
        test_args_dict.update(
            {
                f"Only included Tax for {move_type}": (
                    move_type,
                    included_tax,
                    included_error_parts,
                )
                for move_type in move_types
            }
        )
        test_args_dict.update(
            {
                f"No extra Tax for {move_type}": (
                    move_type,
                    self.env["account.tax"].browse(),
                    None,
                )
                for move_type in move_types
            }
        )

        for test_name, test_args in test_args_dict.items():
            with self.subTest(msg=test_name):
                self._assert_invoice_validation(*test_args)
