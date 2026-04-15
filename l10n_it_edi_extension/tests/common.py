#  Copyright 2024 Simone Rubino - Aion Tech
#  Copyright 2025 Simone Rubino
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from odoo import tools
from odoo.fields import Command

from odoo.addons.l10n_it_edi.tests.common import TestItEdi


class Common(TestItEdi):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.module = "l10n_it_edi_extension"

        cls.italian_shipping_partner_a = cls.env["res.partner"].create(
            {
                "name": "Mario Rossi Shipping",
                "country_id": cls.env.ref("base.it").id,
                "street": "Largo S. Martino 1",
                "zip": "80129",
                "city": "Napoli",
                "company_id": False,
                "invoice_edi_format": "it_edi_xml",
            }
        )
        cls.us_partner = cls.env["res.partner"].create(
            {
                "name": "US Partner",
                "city": "Test city",
                "country_id": cls.env.ref("base.us").id,
                "zip": "12345",
                "street": "123 Rainbow Road",
                "company_id": False,
                "is_company": True,
            }
        )
        cls.us_shipping_partner = cls.env["res.partner"].create(
            {
                "name": "US Partner Shipping",
                "city": "New Hartford",
                "country_id": cls.env.ref("base.us").id,
                "street": "1000 Burrstone Rd",
                "zip": "13413",
                "company_id": False,
            }
        )
        cls.split_payment_tax = (
            cls.env["account.tax"]
            .with_company(cls.company)
            .search([("name", "=", "22% SP")])
        )
        cls.tax_zero_percent_us = (
            cls.env["account.tax"]
            .with_company(cls.company)
            .create(
                {
                    "name": "0 % US",
                    "amount": 0.0,
                    "amount_type": "percent",
                    "l10n_it_exempt_reason": "N3.1",
                    "l10n_it_law_reference": "Art. 8, c.1, lett.a - D.P.R. 633/1972",
                }
            )
        )
        cls.n32_sale_tax = (
            cls.env["account.tax"]
            .with_company(cls.company)
            .create(
                {
                    "name": "0 % with N3.2",
                    "amount": 0.0,
                    "amount_type": "percent",
                    "l10n_it_exempt_reason": "N3.2",
                    "l10n_it_law_reference": "N3.2 tax law reference",
                    "type_tax_use": "sale",
                    "invoice_repartition_line_ids": cls.repartition_lines(
                        cls.RepartitionLine(100, "base", ("+03", "+vj3")),
                        cls.RepartitionLine(100, "tax", ("+5v",)),
                        cls.RepartitionLine(-100, "tax", ("-4v",)),
                    ),
                    "refund_repartition_line_ids": cls.repartition_lines(
                        cls.RepartitionLine(100, "base", ("-03", "-vj3")),
                        cls.RepartitionLine(100, "tax", False),
                        cls.RepartitionLine(-100, "tax", False),
                    ),
                }
            )
        )
        cls.default_product = cls.env["product.product"].create(
            {
                "name": "Test default Product",
                "supplier_taxes_id": [
                    Command.create(
                        {
                            "name": "Test purchase tax in default product",
                            "amount": 22,
                            "sequence": 100,
                            "type_tax_use": "purchase",
                            "company_id": cls.company.id,
                        }
                    )
                ],
            }
        )
        cls.default_product.with_company(cls.company).property_account_expense_id = (
            cls.env["account.account"]
            .with_company(cls.company)
            .create(
                {
                    "name": "Test expense account in default product",
                    "code": "TESTEADP",
                    "account_type": "expense",
                }
            )
        )

    def _import_moves_from_zip(self, zip_name):
        path = f"{self.module}/tests/import_xmls/{zip_name}"
        with tools.file_open(path, mode="rb") as file:
            encoded_file = base64.encodebytes(file.read())

        wizard_attachment_import = (
            self.env["l10n_it_edi.import_file_wizard"]
            .with_company(self.company)
            .create(
                {
                    "l10n_it_edi_attachment_filename": zip_name,
                    "l10n_it_edi_attachment": encoded_file,
                }
            )
        )
        action = wizard_attachment_import.action_import()

        move_ids = action.get("domain")[0][2]
        return self.env["account.move"].browse(move_ids)
