#  Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.l10n_it_edi_extension.tests.common import Common as EdiCommon


class Common(EdiCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.module = "l10n_it_edi_accompanying_invoice"

        cls.italian_delivery_carrier = cls.env["res.partner"].create(
            {
                "name": "Italian Carrier",
                "vat": "IT66068360081",
                "country_id": cls.env.ref("base.it").id,
                "company_id": False,
                "is_company": True,
            }
        )
