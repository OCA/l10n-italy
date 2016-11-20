# -*- coding: utf-8 -*-
# Copyright 2014 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# Copyright 2016 Andrea Gallina (Apulia Software)
# Copyright 2016 Giuliano Lotta
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestFiscalCodeWizard(TransactionCase):
    """ Each test method is run independently and the database transaction
    is rolled back after each.
    """

    def setUp(self):
        """initializes the self.env attribute The test runner will
        run then the tests one after the other with a call to setUp()
        before each test method and a call to tearDown() after each
        To test the fiscal code for a private citizen, se need to create
        a transient partner with is_company = False
        """
        super(TestFiscalCodeWizard, self).setUp()
        partner_model = self.env['res.partner']
        self.partner = partner_model.create(
            {'name': u'Rossi Mario',
             'email': u"mario.rossi@gmail.com",
             'is_company': False, })

    def test_fiscalcode_normal(self):
        """ test that for a private citizen the fiscal code is
        computed correctly
        """
        # ROMA (RM)
        wizard = self.env['wizard.compute.fc'].with_context(
            active_id=self.partner.id).create({
                'fiscalcode_surname': 'ROSSI',
                'fiscalcode_firstname': 'MARIO',
                'birth_date': '1984-06-04',
                'sex': 'M',
                'birth_city': 10048,
                'birth_province': 10048,
            })
        # ---- Compute FiscalCode
        wizard.compute_fc()
        self.assertEqual(self.partner.fiscalcode, 'RSSMRA84H04H501X')

        # test for a  fiscal code when city is categorized ad ORA
        # e.g. AbanoBagni (PD) - Notes = ORA
        self.partner.fiscalcode = None
        wizard = self.env['wizard.compute.fc'].with_context(
            active_id=self.partner.id).create({
                'fiscalcode_surname': 'ROSSI',
                'fiscalcode_firstname': 'MARIO',
                'birth_date': '1984-06-04',
                'sex': 'M',
                'birth_city': 1,
                'birth_province': 8379,
            })
        # ---- Compute FiscalCode
        wizard.compute_fc()
        self.assertEqual(self.partner.fiscalcode, 'RSSMRA84H04A001E')

        # test for a  fiscal code when city is categorized ad VED
        # e.g. Abbadia (CO) - Notes = VED
        self.partner.fiscalcode = None
        wizard = self.env['wizard.compute.fc'].with_context(
            active_id=self.partner.id).create({
                'fiscalcode_surname': 'ROSSI',
                'fiscalcode_firstname': 'MARIO',
                'birth_date': '1984-06-04',
                'sex': 'M',
                'birth_city': 3,
                'birth_province': 3975,
            })
        # ---- Compute FiscalCode
        wizard.compute_fc()
        self.assertEqual(self.partner.fiscalcode, 'RSSMRA84H04A005R')

        # test for a  fiscal code when city is categorized ad AGG
        #  e.g. AbbadiaSopraAdda (CO) - Notes = AGG
        self.partner.fiscalcode = None
        wizard = self.env['wizard.compute.fc'].with_context(
            active_id=self.partner.id).create({
                'fiscalcode_surname': 'ROSSI',
                'fiscalcode_firstname': 'MARIO',
                'birth_date': '1984-06-04',
                'sex': 'M',
                'birth_city': 4,
                'birth_province': 3975,
            })
        # ---- Compute FiscalCode
        wizard.compute_fc()
        self.assertEqual(self.partner.fiscalcode, 'RSSMRA84H04A005R')

        # test for a  fiscal code when city is categorized ad AGP
        # e.g. Bressana (PV) - Notes = AGP
        self.partner.fiscalcode = None
        wizard = self.env['wizard.compute.fc'].with_context(
            active_id=self.partner.id).create({
                'fiscalcode_surname': 'ROSSI',
                'fiscalcode_firstname': 'MARIO',
                'birth_date': '1984-06-04',
                'sex': 'M',
                'birth_city': 531,
                'birth_province': 8593,
            })
        # ---- Compute FiscalCode
        wizard.compute_fc()
        self.assertEqual(self.partner.fiscalcode, 'RSSMRA84H04B159E')
