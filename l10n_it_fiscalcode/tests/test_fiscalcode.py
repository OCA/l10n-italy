# Copyright 2023 Simone Rubino - TAKOBI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestFiscalCode(TransactionCase):

    def setUp(self):
        super(TestFiscalCode, self).setUp()

        self.partner = self.env.ref('base.res_partner_2')
        self.rome_province = self.env.ref('base.state_it_rm')

    def test_fiscalcode_compute(self):
        wizard = self.env['wizard.compute.fc'].with_context(
            active_id=self.partner.id).create({
                'fiscalcode_surname': 'ROSSI',
                'fiscalcode_firstname': 'MARIO',
                'birth_date': '1984-06-04',
                'sex': 'M',
                'birth_city': 10048,
                'birth_province': self.rome_province.id
            })
        # ---- Compute FiscalCode
        wizard.compute_fc()
        self.assertEqual(self.partner.fiscalcode, 'RSSMRA84H04H501X')

    def test_fiscalcode_check(self):
        # Wrong FC length
        with self.assertRaises(ValidationError):
            self.env['res.partner'].create({
                'name': 'Person',
                'is_company': False,
                'fiscalcode': '123',
            })
        # Correct FC
        self.env['res.partner'].create({
            'name': 'Person',
            'is_company': False,
            'fiscalcode': 'RSSMRA84H04H501X',
        })
        # Empty FC
        self.env['res.partner'].create({
            'name': 'Person',
        })
        # FC is VAT number
        self.env['res.partner'].create({
            'name': 'Person',
            'company_name': 'Company',
            'is_company': False,
            'fiscalcode': '12345670017',
        })
        # Invalid FC
        with self.assertRaises(ValidationError):
            self.env["res.partner"].create(
                {
                    "name": "Person",
                    "is_company": False,
                    "fiscalcode": "AAAMRA00H04H5010",
                }
            )

    def test_company_fiscal_code(self):
        base_company_partner_values = {
            'name': 'Company',
            'is_company': True,
        }

        wrong_fiscal_code_partner_values = dict(
            **base_company_partner_values,
            fiscalcode='123456789',
        )
        with self.assertRaises(ValidationError):
            self.env['res.partner'].create(wrong_fiscal_code_partner_values)

        correct_fiscal_code_partner_values = dict(
            **base_company_partner_values,
            fiscalcode='12345670017',
        )
        self.env['res.partner'].create(correct_fiscal_code_partner_values)

        empty_fiscal_code_partner_values = base_company_partner_values.copy()
        self.env['res.partner'].create(empty_fiscal_code_partner_values)