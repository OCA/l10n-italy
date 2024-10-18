# Copyright 2023 Marco Colombo <marco.colombo@phi.technology>

from odoo.exceptions import UserError
from odoo.tests import tagged

from .fatturapa_common import FatturaPACommon


@tagged("post_install", "-at_install")
class TestFatturaPAPreventiveChecks(FatturaPACommon):
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

    def test_1_missing_taxes(self):
        self.env.company.fatturapa_pub_administration_ref = "F000000111"
        self.set_sequences(13, "2016-01-07")
        invoice = self.invoice_model.create(
            {
                "partner_id": self.res_partner_fatturapa_0.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": self.a_sale.id,
                            "product_id": self.product_product_10.id,
                            "name": "Mouse\nOptical",
                            "quantity": 1,
                            "product_uom_id": self.product_uom_unit.id,
                            "price_unit": 10,
                            "tax_ids": [(5, 0, 0)],
                        },
                    ),
                ],
            }
        )
        invoice._post()
        with self.assertRaises(UserError) as ue:
            self.run_wizard(invoice.id)
        error_message = "Invoice {} contains product lines w/o taxes".format(
            invoice.name
        )
        self.assertEqual(ue.exception.args[0], error_message)

        # test lack of exemption kind
        tax_0 = self.tax_00_ns.copy()
        tax_0.name = "Exempt (test)"
        former_kind_id = tax_0.kind_id
        tax_0.kind_id = False

        invoice = invoice.copy()
        invoice.invoice_line_ids[0].tax_ids = [(6, 0, [tax_0.id])]
        invoice._post()
        error_message = (
            "Invoice {}: a tax exemption kind must be specified for tax {}".format(
                invoice.name, tax_0.name
            )
        )
        with self.assertRaises(UserError) as ue:
            self.run_wizard(invoice.id)
        self.assertEqual(ue.exception.args[0], error_message)

        # test lack of law_reference
        tax_0.kind_id = former_kind_id
        tax_0.law_reference = False

        invoice = invoice.copy()
        invoice.invoice_line_ids[0].tax_ids = [(6, 0, [tax_0.id])]
        invoice._post()

        error_message = (
            "Invoice {}: the law reference must be specified for tax {}".format(
                invoice.name, tax_0.name
            )
        )
        with self.assertRaises(UserError) as ue:
            self.run_wizard(invoice.id)
        self.assertEqual(ue.exception.args[0], error_message)
