from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


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
