# -*- coding: utf-8 -*-
# Copyright 2016 Davide Corio (Abstract)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class BankCase(TransactionCase):

    def setUp(self):
        super(BankCase, self).setUp()
        self.partner1 = self.env['res.partner'].create({'name': 'Partner1'})

    def test_create_bank(self):
        bank_model = self.env['res.bank']
        pbank_model = self.env['res.partner.bank']
        bank1 = bank_model.create({
            'name': 'Bank1',
            'abi': 'abi_1',
            'cab': 'cab_1',
            })
        pbank1 = pbank_model.create({
            'acc_number': '212',
            'partner_id': self.partner1.id,
            'bank_id': bank1.id,
            })
        pbank1.onchange_bank_id()
        self.assertEqual(pbank1.bank_abi, 'abi_1')
        self.assertEqual(pbank1.bank_cab, 'cab_1')
