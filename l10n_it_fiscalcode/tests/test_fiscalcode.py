# -*- coding: utf-8 -*-
# Copyright 2014 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# Copyright 2016 Andrea Gallina (Apulia Software)
# Copyright 2016 Giuliano Lotta
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestFiscalCode(TransactionCase):
    # Each test method is run independently and the database transaction
    # is rolled back after each.
    def setUp(self):
        """initializes the self.env attribute The test runner will
        run then one after the other with a call to setUp() before
        each test method and a call to tearDown() after each
        """
        super(TestFiscalCode, self).setUp()
        # get Italian and French country_id for
        # Italian citizen/companies creation
        self.italy_id = self.env['res.country'].search([(
            'code', '=', 'IT')])[0].id
        self.france_id = self.env['res.country'].search([(
            'code', '=', 'FR')])[0].id

# -------------------------------------------------------------------

    def test_company(self):
        """ Test a company partner
        with Empty, correct and wrong fiscalcode
        """
        # No FiscalCode
        record = self.env['res.partner'].create(
            {'name': u'Test0 Italian Company',
             'email': u"foo@gmail.com",
             'is_company': True,
             'is_soletrader': False,
             'country_id': self.italy_id,
             'fiscalcode': "",
             })
        self.assertEqual(record.fiscalcode, "")

        # Italian company has the fiscalcode like a VAT number
        record = self.env['res.partner'].create(
            {'name': u'Test1 Italian Company',
             'email': u"foo@gmail.com",
             'is_company': True,
             'is_soletrader': False,
             'country_id': self.italy_id,
             'fiscalcode': u'12345678901',
             })
        self.assertEqual(record.fiscalcode, '12345678901')

        # WRONG length FiscalCode for a company
        with self.assertRaises(ValidationError):
            record = self.env['res.partner'].create(
                {'name': u'Test2 Italian Company',
                 'email': u"foo@gmail.com",
                 'is_company': True,
                 'is_soletrader': False,
                 'country_id': self.italy_id,
                 'fiscalcode': u"1234567890123456",
                 })


        # Wrong Chars FiscalCode (alphabetic)
        with self.assertRaises(ValidationError):
            record = self.env['res.partner'].create(
                {'name': u'Test3 Italian Company',
                 'email': u"foo@gmail.com",
                 'is_company': True,
                 'is_soletrader': False,
                 'country_id': self.italy_id,
                 'fiscalcode': u"1234567890A",
                 })


        # Wrong country for Italian FiscalCode
        with self.assertRaises(ValidationError):
            record = self.env['res.partner'].create(
                {'name': u'Test4 Italian Company',
                 'email': u"foo@gmail.com",
                 'is_company': True,
                 'is_soletrader': False,
                 'country_id': self.france_id,
                 'fiscalcode': u"12345678901",
                 })


# -------------------------------------------------------------------

    def test_private_citizen(self):
        """ Test private citizen partner
        with Empty, correct and wrong fiscalcode
        """
        # normal fiscalcode for private citizen
        record = self.env['res.partner'].create(
            {'name': u'Test1 Private Italian Citizen',
             'email': u"foo@gmail.com",
             'is_company': False,
             'is_soletrader': False,
             'country_id': self.italy_id,
             'fiscalcode': u'BNZVCN32S10E573Z',
             })
        self.assertEqual(record.fiscalcode, 'BNZVCN32S10E573Z')

        # special fiscalcode with omocodia for private citizen
        # last "3" character, become a "P" char because of omocodia
        # CRC code changes accordingly
        record = self.env['res.partner'].create(
            {'name': u'Test2 Private Italian Citizen Omocod.',
             'email': u"foo@gmail.com",
             'is_company': False,
             'is_soletrader': False,
             'country_id': self.italy_id,
             'fiscalcode': u'BNZVCN32S10E57PV',
             })
        self.assertEqual(record.fiscalcode, 'BNZVCN32S10E57PV')

        # Private citizen No FiscalCode
        record = self.env['res.partner'].create(
            {'name': u'Test4 No FiscalCode',
             'email': u"foo@gmail.com",
             'is_company': False,
             'is_soletrader': False,
             'country_id': self.italy_id,
             'fiscalcode': "",
             })
        self.assertEqual(record.fiscalcode, "")

        # WRONG Private Citizen FiscalCode
        with self.assertRaises(ValidationError):
            record = self.env['res.partner'].create(
                {'name': u'Test4 No FiscalCode',
                 'email': u"foo@gmail.com",
                 'is_company': False,
                 'is_soletrader': False,
                 'country_id': self.italy_id,
                 'fiscalcode': u"1234567890123456",
                 })


        # WRONG Private Citizen country
        with self.assertRaises(ValidationError):
            record = self.env['res.partner'].create(
                {'name': u'Test4 No FiscalCode',
                 'email': u"foo@gmail.com",
                 'is_company': False,
                 'is_soletrader': False,
                 'country_id': self.france_id,
                 'fiscalcode': u"BNZVCN32S10E573Z",
                 })


# -------------------------------------------------------------------

    def test_soletrader(self):
        """ Test sole trader partner
        with Empty    , correct and wrong fiscalcode
        """
        # normal fiscalcode for private citizen
        record = self.env['res.partner'].create(
            {'name': u'Test1 Private Italian Citizen',
             'email': u"foo@gmail.com",
             'is_company': True,
             'is_soletrader': True,
             'country_id': self.italy_id,
             'fiscalcode': u'BNZVCN32S10E573Z',
             })
        self.assertEqual(record.fiscalcode, 'BNZVCN32S10E573Z')

        # special fiscalcode with omocodia for private citizen
        # last "3" character, become a "P" char because of omocodia
        # CRC code changes accordingly
        record = self.env['res.partner'].create(
            {'name': u'Test2 Private Italian Citizen Omocod.',
             'email': u"foo@gmail.com",
             'is_company': True,
             'is_soletrader': True,
             'country_id': self.italy_id,
             'fiscalcode': u'BNZVCN32S10E57PV',
             })
        self.assertEqual(record.fiscalcode, 'BNZVCN32S10E57PV')

        # Private citizen No FiscalCode
        record = self.env['res.partner'].create(
            {'name': u'Test4 No FiscalCode',
             'email': u"foo@gmail.com",
             'is_company': True,
             'is_soletrader': True,
             'country_id': self.italy_id,
             'fiscalcode': "",
             })
        self.assertEqual(record.fiscalcode, "")

        # WRONG Private Citizen FiscalCode
        with self.assertRaises(ValidationError):
            record = self.env['res.partner'].create(
                {'name': u'Test4 No FiscalCode',
                 'email': u"foo@gmail.com",
                 'is_company': True,
                 'is_soletrader': True,
                 'country_id': self.italy_id,
                 'fiscalcode': u"1234567890123456",
                 })

        # WRONG Private Citizen country
        with self.assertRaises(ValidationError):
            record = self.env['res.partner'].create(
                {'name': u'Test4 No FiscalCode',
                 'email': u"foo@gmail.com",
                 'is_company': True,
                 'is_soletrader': True,
                 'country_id': self.france_id,
                 'fiscalcode': u"BNZVCN32S10E573Z",
                 })

# -------------------------------------------------------------------

    def test_onchange_iscompany(self):
        """ Test that when is_com0pany is switched from True to False
         is_soletrader is also set to False
        """
        # Get an empty recordset
        partner = self.env['res.partner']
        # Prepare the values to create a new  record
        values = {'name': u'OnChange Test',
                  'email': u"foo@gmail.com",
                  'is_company': False,
                  'is_soletrader': True,
                  'country_id': self.italy_id,
                  'fiscalcode': u'BNZVCN32S10E573Z',
                  }
        # Retrieve the onchange specifications
        specs = partner._onchange_spec()
        # Get the result of the onchange method for is_company field:
        updates = partner.onchange(values, ['is_company'], specs)
        # value  is a dictionary of newly computed field values.
        # This dictionary only features keys that are in the values parameter
        # passed to onchange().
        new_values = updates.get('value', {})
        # check values computed by the onchange.
        self.assertEqual(new_values['is_soletrader'], False)
