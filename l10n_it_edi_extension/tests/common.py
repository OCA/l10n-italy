#  Copyright 2024 Simone Rubino - Aion Tech
#  Copyright 2025 Simone Rubino
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


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
