# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase

from odoo.addons.l10n_it_account.tools.account_tools import fpa_schema_get_enum


class TestAccountTaxKind(TransactionCase):
    def setUp(self):
        super(TestAccountTaxKind, self).setUp()
        self.tax_kind_n1 = self.env.ref("l10n_it_account_tax_kind.n1")

    def test_compute_display_name(self):
        self.tax_kind_n1._compute_display_name()
        self.assertEqual(
            self.tax_kind_n1.display_name,
            "[{}] {}".format(self.tax_kind_n1.code, self.tax_kind_n1.name),
        )

    def test_name_search(self):
        result = self.env["account.tax.kind"].name_search("Escluse ex art. 15")
        self.assertEqual(result and result[0][0], self.tax_kind_n1.id)

    def test_compare_with_fpa_schema(self):
        """Check that the values we define in this module are
        the same as those defined in FPA xsd"""

        my_codes = self.env["account.tax.kind"].search([]).mapped("code")

        # from fatturapa xml Schema
        xsd_codes = [code for code, descr in fpa_schema_get_enum("NaturaType")]

        self.assertCountEqual(my_codes, xsd_codes)
