# -*- coding: utf-8 -*-
# Copyright 2017 Lorenzo Battistini
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase


class TestDocType(TransactionCase):

    def setUp(self):
        super(TestDocType, self).setUp()
        self.journalrec = self.env['account.journal'].search(
            [('type', '=', 'sale')])[0]
        self.TD01 = self.env.ref('l10n_it_fiscal_document_type.1')
        self.inv_model = self.env['account.invoice']
        self.partner3 = self.env.ref('base.res_partner_3')

    def test_doc_type(self):
        self.TD01.journal_ids = [self.journalrec.id]
        invoice = self.inv_model.create({
            'partner_id': self.partner3.id
        })
        invoice._set_document_fiscal_type()
        self.assertEqual(invoice.fiscal_document_type_id.id, self.TD01.id)

        invoice2 = self.inv_model.create({
            'partner_id': self.partner3.id
        })
        self.assertEqual(invoice2.fiscal_document_type_id.id, self.TD01.id)
