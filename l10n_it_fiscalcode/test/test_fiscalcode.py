# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Luigi Di Naro
#    Copyright 2016 KTec S.r.l.
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
##############################################################################

from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError

class TestFiscalcode(TransactionCase):

    def test_company_characterfc(self):
        record = self.env['res.partner'].create({'name': 'Test Partner',
                                                 'is_company' : True,
                                                 'fiscalcode':'123abc'})
        self.assertRaises(ValidationError)

    def test_company_fclenght(self):
        record = self.env['res.partner'].create({'name': 'Test Partner',
                                                 'is_company' : True,
                                                 'fiscalcode':'123456789'})
        self.assertRaises(ValidationError)

    def test_company_fcok(self):
        record = self.env['res.partner'].create({'name': 'Test Partner',
                                                 'is_company' : True,
                                                 'fiscalcode':'12345678901'})
        self.assertEqual(record.fiscalcode,'12345678901')

    def test_company_individualfc_ok(self):
        record = self.env['res.partner'].create({'name': 'Test Partner',
                                                 'is_company': True,
                                                 'individual': True,
                                                 'fiscalcode':'RSSMRA85T10A562S'})
        self.assertEqual(record.fiscalcode,'RSSMRA85T10A562S')

    def test_company_individualfc_ko(self):
        record = self.env['res.partner'].create({'name': 'Test Partner',
                                                 'is_company': True,
                                                 'individual': True,
                                                 'fiscalcode':'RSSMRA85T10A562X'})
        self.assertRaises(ValidationError)

    def test_individualfc_ok(self):
        record = self.env['res.partner'].create({'name': 'Test Partner',
                                                 'is_company': False,
                                                 'fiscalcode':'RSSMRA85T10A562S'})
        self.assertEqual(record.fiscalcode,'RSSMRA85T10A562S')

    def test_individualfc_ko(self):
        record = self.env['res.partner'].create({'name': 'Test Partner',
                                                 'is_company': False,
                                                 'fiscalcode':'RSSMRA85T10A562'})
        self.assertRaises(ValidationError)