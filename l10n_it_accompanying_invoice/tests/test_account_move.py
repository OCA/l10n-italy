#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestAccountMove(AccountTestInvoicingCommon):
    def test_propagate_partner_values(self):
        """Create an invoice for a partner,
        shipping values are propagated from the partner to the invoice."""
        # Arrange
        partner = self.env.ref("base.res_partner_1")
        partner.default_transport_condition_id = self.env.ref(
            "l10n_it_delivery_note_base.transport_condition_PF"
        )
        partner.default_goods_appearance_id = self.env.ref(
            "l10n_it_delivery_note_base.goods_appearance_CAR"
        )
        partner.default_transport_reason_id = self.env.ref(
            "l10n_it_delivery_note_base.transport_reason_VEN"
        )
        partner.default_transport_method_id = self.env.ref(
            "l10n_it_delivery_note_base.transport_method_MIT"
        )

        # Act
        invoice = self.init_invoice(
            "out_invoice",
            partner=partner,
        )

        # Assert
        self.assertEqual(
            invoice.delivery_transport_condition_id,
            partner.default_transport_condition_id,
        )
        self.assertEqual(
            invoice.delivery_goods_appearance_id,
            partner.default_goods_appearance_id,
        )
        self.assertEqual(
            invoice.delivery_transport_reason_id,
            partner.default_transport_reason_id,
        )
        self.assertEqual(
            invoice.delivery_transport_method_id,
            partner.default_transport_method_id,
        )
