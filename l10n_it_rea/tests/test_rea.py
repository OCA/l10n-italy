#  Copyright 2021 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestRea(TransactionCase):

    def setUp(self):
        super(TestRea, self).setUp()
        self.company = self.env.ref('base.main_company')
        self.rome_province = self.env.ref('base.state_it_rm')
        self.partner_model = self.env['res.partner']
        self.rea_partner = self.create_rea_partner()

    def create_rea_partner(self):
        return self.partner_model.create({
            'name': "REA test partner",
            'rea_code': 'test_rea_code',
            'rea_office': self.ref('base.state_it_rm')
        })

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

    def test_unique_constraint(self):
        """Check that another partner with same
        REA Code and Office Province cannot be created."""
        with self.assertRaises(ValidationError):
            self.create_rea_partner()

    def test_archived_unique_constraint(self):
        """Check that another partner with same
        REA Code and Office Province can be created
        if it is the only one active."""
        self.rea_partner.active = False
        self.create_rea_partner()
        rea_domain = [
            ('rea_office', '=', self.rea_partner.rea_office.id),
            ('rea_code', '=', self.rea_partner.rea_code),
            ('company_id', '=', self.rea_partner.company_id.id),
        ]

        self.assertEqual(
            self.partner_model.search_count(rea_domain),
            1
        )
        self.assertEqual(
            self.partner_model
                .with_context(active_test=False)
                .search_count(rea_domain),
            2
        )
