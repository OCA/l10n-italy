# -*- coding: utf-8 -*-
# Copyright 2018 Teuron (<http://www.teuron.it>)

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestFiscalcode(TransactionCase):

    def test_company_characterfc(self):
        self.env['res.partner'].create({'name': 'Test Partner',
                                        'is_company': True,
                                        'fiscalcode': '123abc'})
        self.assertRaises(ValidationError)

    def test_company_fclenght(self):
        self.env['res.partner'].create({'name': 'Test Partner',
                                        'is_company': True,
                                        'fiscalcode': '123456789A'})
        self.assertRaises(ValidationError)

    def test_company_fcok(self):
        p = self.env['res.partner'].create({'name': 'Test Partner',
                                            'is_company': True,
                                            'fiscalcode': '12345678901'})
        self.assertEqual(p.fiscalcode, '12345678901')

    def test_company_individualfc_ok(self):
        p = self.env['res.partner'].create({'name': 'Test Partner',
                                            'is_company': True,
                                            'is_individual': True,
                                            'fiscalcode': 'RSSMRA85T10A562S'})
        self.assertEqual(p.fiscalcode, 'RSSMRA85T10A562S')

    def test_company_individualfc_ko(self):
        self.env['res.partner'].create({'name': 'Test Partner',
                                        'is_company': True,
                                        'is_individual': True,
                                        'fiscalcode': 'RSSMRA85T10A562X'})
        self.assertRaises(ValidationError)

    def test_individualfc_ok(self):
        p = self.env['res.partner'].create({'name': 'Test Partner',
                                            'is_company': False,
                                            'fiscalcode': 'RSSMRA85T10A562S'})
        self.assertEqual(p.fiscalcode, 'RSSMRA85T10A562S')

    def test_individualfc_ko(self):
        self.env['res.partner'].create({'name': 'Test Partner',
                                        'is_company': False,
                                        'fiscalcode': 'RSSMRA85T10A562'})
        self.assertRaises(ValidationError)
