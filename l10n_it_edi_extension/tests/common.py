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
