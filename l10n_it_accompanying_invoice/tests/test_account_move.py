#  Copyright 2023 Simone Rubino - Aion Tech
#  Copyright 2025 Simone Rubino
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestAccountMove(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        partner = cls.env["res.partner"].create(
            {
                "name": "Wood Corner",
                "is_company": True,
                "street": "1839 Arbor Way",
                "city": "Turlock",
                "state_id": cls.env.ref("base.state_us_5").id,
                "zip": "95380",
                "email": "wood.corner26@example.com",
                "phone": "(623)-853-7197",
                "vat": "US12345672",
            }
        )

        partner.default_transport_condition_id = cls.env.ref(
            "l10n_it_delivery_note.transport_condition_PF"
        )
        partner.default_goods_appearance_id = cls.env.ref(
            "l10n_it_delivery_note.goods_appearance_CAR"
        )
        partner.default_transport_reason_id = cls.env.ref(
            "l10n_it_delivery_note.transport_reason_VEN"
        )
        partner.default_transport_method_id = cls.env.ref(
            "l10n_it_delivery_note.transport_method_MIT"
        )

    def test_propagate_partner_values(self):
        """Create an invoice for a partner,
        shipping values are propagated from the partner to the invoice."""
        # Act
        invoice = self.init_invoice(
            "out_invoice",
            partner=self.partner,
        )

        # Assert
        self.assertEqual(
            invoice.delivery_transport_condition_id,
            self.partner.default_transport_condition_id,
        )
        self.assertEqual(
            invoice.delivery_goods_appearance_id,
            self.partner.default_goods_appearance_id,
        )
        self.assertEqual(
            invoice.delivery_transport_reason_id,
            self.partner.default_transport_reason_id,
        )
        self.assertEqual(
            invoice.delivery_transport_method_id,
            self.partner.default_transport_method_id,
        )
