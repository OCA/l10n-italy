# Copyright 2018 Simone Rubino - Agile Business Group
# Copyright 2022 Simone Rubino - TAKOBI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from unittest.mock import patch

from odoo.tests.common import TransactionCase

from .test_nuts_request_results import create_response_ok

MOCK_PATH = "odoo.addons.base_location_nuts.wizard.nuts_import.requests.get"


class TestNUTS(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        importer = cls.env["nuts.import"].create([{}])
        with patch(MOCK_PATH, return_value=create_response_ok()):
            importer.import_update_partner_nuts()
        cls.rome_nuts = cls.env["res.partner.nuts"].search([("code", "=", "ITI43")])
        rome_state_id = cls.env.ref("base.state_it_rm").id
        cls.it_partner = cls.env["res.partner"].create({"name": "it_partner"})
        cls.it_partner.write({"state_id": rome_state_id})

    def test_italian_nuts(self):
        """
        Check that onchange method correctly bind level 4 nuts with
        italian states.
        """
        self.it_partner.onchange_state_id_base_location_nuts()
        self.assertEqual(self.it_partner.state_id, self.it_partner.nuts4_id.state_id)
