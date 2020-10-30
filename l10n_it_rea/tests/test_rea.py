# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestRea(TransactionCase):

    def setUp(self):
        super(TestRea, self).setUp()
        self.company = self.env.ref('base.main_company')
        self.rome_province = self.env.ref('base.state_it_rm')

    def test_rea_data(self):
        self.company.rea_office = self.rome_province.id
        self.company.rea_code = '123456'
        self.company.rea_capital = 10000
        self.company.rea_member_type = 'SU'
        self.company.rea_liquidation_state = 'LN'
        self.company.onchange_rea_data()
        self.assertEqual(
            self.company.company_registry,
            'RM - 123456 / Share Cap. 10,000.00 € / '
            'Unique Member / Not in liquidation'
        )
        self.assertEqual(
            self.company.partner_id.rea_office, self.company.rea_office)
        self.assertEqual(
            self.company.partner_id.rea_code, self.company.rea_code)
        self.assertEqual(
            self.company.partner_id.rea_capital, self.company.rea_capital)
        self.assertEqual(
            self.company.partner_id.rea_member_type,
            self.company.rea_member_type)
        self.assertEqual(
            self.company.partner_id.rea_liquidation_state,
            self.company.rea_liquidation_state)
