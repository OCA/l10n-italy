from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class TestFatturapa(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.invoice_model = cls.env["account.move"]
        cls.partner = cls.env.ref("base.res_partner_2")
        cls.product = cls.env.ref("product.product_product_4")
        cls.fatturapa_payment_method = cls.env.ref(
            "l10n_it_fiscal_payment_term.fatturapa_mp12"
        )
        cls.payment_term = cls.env["account.payment.term"].create(
            {
                "name": "RiBa",
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "value": "balance",
                            "value_amount": 0.0,
                            "sequence": 10,
                            "days": 0,
                            "option": "after_invoice_month",
                        },
                    ),
                ],
                "fatturapa_pm_id": cls.fatturapa_payment_method.id,
            }
        )
        cls.bank = cls.env["res.bank"].create(
            {
                "name": "Bank",
            }
        )
        cls.partner_bank = cls.env["res.partner.bank"].create(
            {
                "acc_number": "IT49 A000 0123 4567 0000 0000 0000",
                "sanitized_acc_number": "IT49A000012345670000000000000000",
                "partner_id": cls.partner.id,
                "bank_id": cls.bank.id,
            }
        )

    def test_create_invoice_with_riba_validation_error(self):
        # Create an invoice with partner bank and RiBa payment mode
        with self.assertRaises(ValidationError) as ve:
            self.invoice_model.create(
                {
                    "move_type": "out_invoice",
                    "partner_bank_id": self.partner_bank.id,
                    "invoice_payment_term_id": self.payment_term.id,
                    "partner_id": self.partner.id,
                    "invoice_line_ids": [
                        (
                            0,
                            0,
                            {
                                "product_id": self.product.id,
                                "quantity": 1,
                                "price_unit": 100,
                            },
                        )
                    ],
                }
            )
        exc_message = ve.exception.args[0]
        self.assertEqual(
            exc_message,
            "It is not possible to set a partner "
            "bank with RIBA payment mode for customer invoices."
            " Please remove the partner bank or change the payment mode.",
        )

    def test_write_invoice_with_riba_validation_error(self):
        # Create an invoice withut Riba ValidationError
        invoice = self.invoice_model.create(
            {
                "move_type": "out_invoice",
                "invoice_payment_term_id": self.payment_term.id,
                "partner_id": self.partner.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "quantity": 1,
                            "price_unit": 100,
                        },
                    )
                ],
            }
        )
        # Add a partner bank to check if the ValidationError is raised
        with self.assertRaises(ValidationError) as ve:
            invoice.write(
                {
                    "partner_bank_id": self.partner_bank.id,
                }
            )
        exc_message = ve.exception.args[0]
        self.assertEqual(
            exc_message,
            "It is not possible to set a partner "
            "bank with RIBA payment mode for customer invoices."
            " Please remove the partner bank or change the payment mode.",
        )
