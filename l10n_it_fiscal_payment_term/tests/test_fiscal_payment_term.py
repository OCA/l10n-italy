# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase

from odoo.addons.l10n_it_account.tools.account_tools import fpa_schema_get_enum


class TestFiscalPaymentTerm(TransactionCase):
    def setUp(self):
        super().setUp()
        self.term_model = self.env["fatturapa.payment_term"]
        self.method_model = self.env["fatturapa.payment_method"]

    def test_compare_terms_with_fpa_schema(self):
        """Check that the values we define in this module are
        the same as those defined in FPA xsd"""

        my_codes = self.term_model.search([]).mapped("code")

        # XXX hardcoded - "" dummy value not in Schema
        my_codes.remove("")

        xsd_codes = [
            code for code, descr in fpa_schema_get_enum("CondizioniPagamentoType")
        ]
        self.assertCountEqual(my_codes, xsd_codes)

    def test_compare_methods_with_fpa_schema(self):
        """Check that the values we define in this module are
        the same as those defined in FPA xsd"""

        my_codes = self.method_model.search([]).mapped("code")
        xsd_codes = [
            code for code, descr in fpa_schema_get_enum("ModalitaPagamentoType")
        ]
        self.assertCountEqual(my_codes, xsd_codes)
