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
        # Wrong FC
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
            'fiscalcode': '123456789',
        })
