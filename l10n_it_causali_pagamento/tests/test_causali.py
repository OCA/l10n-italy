
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
            "B - Utilizzazione economica, da parte dell'autore ..."
        )])

    def test_renaming_causali(self):
        causale_zo = self.env.ref('l10n_it_causali_pagamento.z')
        self.assertEqual(causale_zo.code, 'ZO')
        causale_l = self.env.ref('l10n_it_causali_pagamento.l')
        name = (
            "Redditi derivanti dall’utilizzazione economica di opere "
            "dell’ingegno, di brevetti industriali e di processi, formule e "
            "informazioni relativi a esperienze acquisite in campo "
            "industriale, commerciale o scientifico, che sono percepiti dagli "
            "aventi causa a titolo gratuito (ad es. eredi e "
            "legatari dell’autore e inventore)")
        self.assertEqual(causale_l.name, name)
