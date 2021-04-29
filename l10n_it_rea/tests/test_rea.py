#  -*- coding: utf-8 -*-
#  Copyright 2021 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase


class TestREA (TransactionCase):

    def setUp(self):
        super(TestREA, self).setUp()
        self.partner_model = self.env['res.partner']
        self.rea_partner = self.create_rea_partner()

    def create_rea_partner(self):
        return self.partner_model.create({
            'name': "REA test partner",
            'rea_code': 'test_rea_code',
            'rea_office': self.ref('base.state_it_rm')
        })

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
