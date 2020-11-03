# -*- coding: utf-8 -*-

from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError


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
            "B - Utilizzazione economica, da parte dell'autore ..."
        )])

    def test_renaming_causali(self):
        causale_zo = self.env.ref('l10n_it_causali_pagamento.z')
        self.assertEqual(causale_zo.code, 'ZO')
        causale_l = self.env.ref('l10n_it_causali_pagamento.l')
        name = (
            u"Redditi derivanti dall’utilizzazione economica di opere "
            u"dell’ingegno, di brevetti industriali e di processi, formule e "
            u"informazioni relativi a esperienze acquisite in campo "
            u"industriale, commerciale o scientifico, che sono percepiti dagli "
            u"aventi causa a titolo gratuito (ad es. eredi e "
            u"legatari dell’autore e inventore)")
        self.assertEqual(causale_l.name, name)
