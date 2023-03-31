from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase

from odoo.addons.l10n_it_account.tools.account_tools import fpa_schema_get_enum


class TestReasons(TransactionCase):
    def setUp(self):
        super(TestReasons, self).setUp()
        self.reason_model = self.env["payment.reason"]
        self.reason_b = self.env.ref("l10n_it_payment_reason.b")

    def test_reasons(self):
        with self.assertRaises(ValidationError):
            self.reason_model.create({"code": "B", "name": "Test"})
        name = self.reason_b.name_get()
        self.assertEqual(
            name,
            [
                (
                    self.reason_b.id,
                    "B - Utilizzazione economica, da parte dell'autore ...",
                )
            ],
        )

    def test_compare_with_fpa_schema(self):
        """Check that the values we define in this module are
        the same as those defined in FPA xsd"""

        my_codes = self.reason_model.search([]).mapped("code")

        # from fatturapa xml Schema
        xsd_codes = [
            code for code, descr in fpa_schema_get_enum("CausalePagamentoType")
        ]

        # XXX hardcoded - obsolete code, that is still supported by Schema
        xsd_codes.remove("Z")

        self.assertCountEqual(my_codes, xsd_codes)
