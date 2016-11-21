# -*- coding: utf-8 -*-
# Copyright 2014 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# Copyright 2016 Andrea Gallina (Apulia Software)
# Copyright 2016 Giuliano Lotta
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import SingleTransactionCase
from odoo.exceptions import UserError


class TestFiscalCodeWizard(SingleTransactionCase):
    """ TestCase in which all test methods are run in the same transaction,
    the transaction is started with the first test method and
    rolled back at the end of the last.
    """

    def setUp(self):
        """initializes the self.env attribute The test runner will
        run then the tests one after the other with a call to setUp()
        before each test method and a call to tearDown() after each
        To test the fiscal code for a private citizen, se need to create
        a transient partner with is_company = False
        """
        super(TestFiscalCodeWizard, self).setUp()
        self.partner_model = self.env['res.partner']
        self.partner = self.partner_model.create(
            {'name': u'Rossi Mario',
             'email': u"mario.rossi@gmail.com",
             'fiscalcode': None,
             'is_company': False, })
# -----------------------------------------------------------------------

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
        # ---- Compute FiscalCode & Test it
        wizard.compute_fc()
        self.assertEqual(self.partner.fiscalcode, 'RSSMRA84H04H501X')
# -----------------------------------------------------------------------

    def test_fiscalcode_ora(self):
        """ test for a  fiscal code when city is categorized as ORA
         e.g. AbanoBagni (PD) - Notes = ORA
        """
        wizard = self.env['wizard.compute.fc'].with_context(
            active_id=self.partner.id).create({
                'fiscalcode_surname': 'ROSSI',
                'fiscalcode_firstname': 'MARIO',
                'birth_date': '1984-06-04',
                'sex': 'M',
                'birth_city': 1,
                'birth_province': 8379,
            })
        # ---- Compute FiscalCode & Test it
        self.partner.fiscalcode = None
        wizard.compute_fc()
        self.assertEqual(self.partner.fiscalcode, 'RSSMRA84H04A001E')
# -----------------------------------------------------------------------

    def test_fiscalcode_agg(self):
        """ test for a  fiscal code when city is categorized as AGG
        e.g. AbbadiaSopraAdda (CO) - Notes = AGG
        """
        wizard = self.env['wizard.compute.fc'].with_context(
            active_id=self.partner.id).create({
                'fiscalcode_surname': 'ROSSI',
                'fiscalcode_firstname': 'MARIO',
                'birth_date': '1984-06-04',
                'sex': 'M',
                'birth_city': 4,
                'birth_province': 3975,
            })
        # ---- Compute FiscalCode & Test it
        self.partner.fiscalcode = None
        wizard.compute_fc()
        self.assertEqual(self.partner.fiscalcode, 'RSSMRA84H04A005R')
# -----------------------------------------------------------------------

    def test_fiscalcode_agp(self):
        """ test for a  fiscal code when city is categorized as AGP
        e.g. Bressana (PV) - Notes = AGP
        """
        wizard = self.env['wizard.compute.fc'].with_context(
            active_id=self.partner.id).create({
                'fiscalcode_surname': 'ROSSI',
                'fiscalcode_firstname': 'MARIO',
                'birth_date': '1984-06-04',
                'sex': 'M',
                'birth_city': 531,
                'birth_province': 8593,
            })
        # ---- Compute FiscalCode & Test it
        self.partner.fiscalcode = None
        wizard.compute_fc()
        self.assertEqual(self.partner.fiscalcode, 'RSSMRA84H04B159E')
# -----------------------------------------------------------------------

    def test_fiscalcode_error_nomatch(self):
        """ Fiscal code inserted in form doesn't match the computed one
        """
        with self.assertRaises(UserError):
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
            # ---- Compute FiscalCode & Test it
            self.partner.fiscalcode = u'RSSMRA84H04B159E'
            wizard.compute_fc()

# -----------------------------------------------------------------------
    def test_fiscalcode_error_nodata(self):
        """ Main Data missing for fiscalcode computation
        """
        with self.assertRaises(UserError):
            # ROMA (RM)
            wizard = self.env['wizard.compute.fc'].with_context(
                active_id=self.partner.id).create({
                    'fiscalcode_surname': None,
                    'fiscalcode_firstname': None,
                    'birth_date': None,
                    'sex': 'M',
                    'birth_city': 10048,
                    'birth_province': 10048,
                })
            # ---- Compute FiscalCode & Test it
            self.partner.fiscalcode = None
            wizard.compute_fc()
# -----------------------------------------------------------------------

    def test_fiscalcode_error_noprovince(self):
        """ Province missing for ficalcode computation
        """
        with self.assertRaises(UserError):
            # ROMA (RM)
            wizard = self.env['wizard.compute.fc'].with_context(
                active_id=self.partner.id).create({
                    'fiscalcode_surname': 'ROSSI',
                    'fiscalcode_firstname': 'MARIO',
                    'birth_date': '1984-06-04',
                    'sex': 'M',
                    'birth_city': 10048,
                    'birth_province': None,
                })
            # ---- Compute FiscalCode & Test it
            self.partner.fiscalcode = None
            wizard.compute_fc()
# -----------------------------------------------------------------------
