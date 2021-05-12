# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import SavepointCase


class TestNUTS(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestNUTS, cls).setUpClass()
        importer = cls.env['nuts.import']
        importer.run_import()
        cls.rome_nuts = cls.env['res.partner.nuts'].search(
            [('code', '=', 'ITI43')])
        rome_state_id = cls.env.ref('base.state_it_rm').id
        cls.it_partner = cls.env['res.partner'].create({'name': 'it_partner'})
        cls.it_partner.write({'state_id': rome_state_id})

    def test_italian_nuts(self):
        """
        Check that onchange method correctly bind level 4 nuts with
        italian states.
        """
        self.it_partner.onchange_state_id_base_location_nuts()
        self.assertEqual(
            self.it_partner.state_id,
            self.it_partner.nuts4_id.state_id)
