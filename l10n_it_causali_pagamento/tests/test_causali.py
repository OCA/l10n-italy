# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestCausali(TransactionCase):

    def setUp(self):
        super(TestCausali, self).setUp()
        self.causale_model = self.env['causale.pagamento']
        self.causale_b = self.env.ref('l10n_it_causali_pagamento.b')

    def test_causali(self):
        with self.assertRaises(ValidationError):
            self.causale_model.create({
                'code': 'B',
                'name': 'Test'
            })
        name = self.causale_b.name_get()
        self.assertEqual(name, [(
            self.causale_b.id,
            u"B - Utilizzazione economica, da parte dell'autore ..."
        )])
