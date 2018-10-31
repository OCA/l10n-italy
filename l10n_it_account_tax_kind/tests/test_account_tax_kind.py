# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestAccountTaxKind(TransactionCase):

    def setUp(self):
        super(TestAccountTaxKind, self).setUp()
        self.tax_kind_n1 = self.env.ref('l10n_it_account_tax_kind.n1')

    def test_compute_display_name(self):
        self.tax_kind_n1._compute_display_name()
        self.assertEqual(
            self.tax_kind_n1.display_name,
            u'[%s] %s' % (self.tax_kind_n1.code, self.tax_kind_n1.name))

    def test_name_search(self):
        result = self.env['account.tax.kind'].name_search('Escluse ex art. 15')
        self.assertEqual(result and result[0][0], self.tax_kind_n1.id)
