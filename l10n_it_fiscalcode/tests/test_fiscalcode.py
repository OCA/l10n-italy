# -*- coding: utf-8 -*-
# Copyright 2014 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# Copyright 2016 Andrea Gallina (Apulia Software)
# Copyright 2016 Giuliano Lotta
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestFiscalCode(TransactionCase):
    # Each test method is run independently and the database transaction
    # is rolled back after each.
    def setUp(self):
        super(TestFiscalCode, self).setUp()

    def test_newpartner_fiscalcode(self):
        """ save a new partner with a standard fiscalcode,
        omocodia fiscalcode, and VAT fiscalcode (compamy)
        constrain method will check it and grant right to be saved
        """
        # fix test error because no email found during partner creation
        # modification rolled back after TransactionCase end
        partner_root = self.env.ref('base.partner_root')
        partner_root.email = u"foo@gmail.com"

        partner_model = self.env['res.partner'].sudo(
            self.ref('base.partner_root'))

        # get Italian country_id for Italian citizen/companies creation
        italy_id = self.env['res.country'].search('code', '=', 'IT')

        # normal fiscalcode for private citizen
        self.partner = partner_model.create(
            {'name': u'Test1 Private Italian Citizen',
             'email': u"foo@gmail.com",
             'is_company': 'False',
             'country_id': italy_id,
             'fiscalcode': 'BNZVCN32S10E573Z',
             })

        # special fiscalcode with omocodia for private citizen
        # last "3" character, become a "P" because of omocodia
        # CRC code changes accordingly
        self.partner = partner_model.create(
            {'name': u'Test2 Private Italian Citizen',
             'email': u"foo@gmail.com",
             'is_company': 'False',
             'country_id': italy_id,
             'fiscalcode': 'BNZVCN32S10E57PV',
             })

        # Italian company has the fiscalcode like a VAT number
        self.partner = partner_model.create(
            {'name': u'Test3 Italian Company',
             'email': u"foo@gmail.com",
             'is_company': 'True',
             'country_id': italy_id,
             'fiscalcode': '08106710158',
             })
