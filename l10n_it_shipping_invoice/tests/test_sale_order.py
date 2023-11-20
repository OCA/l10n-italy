#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import Form, tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


def _init_sale_order(env, partner, products):
    sale_order_form = Form(env["sale.order"])
    sale_order_form.partner_id = partner
    for product in products:
        with sale_order_form.order_line.new() as line:
            line.product_id = product
    sale_order = sale_order_form.save()
    return sale_order


@tagged("post_install", "-at_install")
class TestSaleOrder(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(
            chart_template_ref=chart_template_ref,
        )
        cls.partner = cls.env.ref("base.res_partner_1")
        cls.product = cls.env.ref("product.product_product_16")
        cls.sale_order = _init_sale_order(cls.env, cls.partner, cls.product)

    def _get_selection_context(self, record):
        return {
            "active_model": record._name,
            "active_ids": record.ids,
            "active_id": record.id,
        }

    def test_propagate_values(self):
        """Create an invoice for a sale order,
        shipping values are propagated from the sale order to the invoice."""
        # Arrange
        sale_order = self.sale_order
        sale_order.default_transport_condition_id = self.env.ref(
            "l10n_it_delivery_note_base.transport_condition_PF"
        )
        sale_order.default_goods_appearance_id = self.env.ref(
            "l10n_it_delivery_note_base.goods_appearance_CAR"
        )
        sale_order.default_transport_reason_id = self.env.ref(
            "l10n_it_delivery_note_base.transport_reason_VEN"
        )
        sale_order.default_transport_method_id = self.env.ref(
            "l10n_it_delivery_note_base.transport_method_MIT"
        )
        sale_order.action_confirm()

        # Act
        order_context = self._get_selection_context(sale_order)
        payment = (
            self.env["sale.advance.payment.inv"]
            .with_context(**order_context)
            .create({})
        )
        payment.create_invoices()

        # Assert
        invoice = sale_order.invoice_ids[0]
        self.assertEqual(
            invoice.delivery_transport_condition_id,
            sale_order.default_transport_condition_id,
        )
        self.assertEqual(
            invoice.delivery_goods_appearance_id,
            sale_order.default_goods_appearance_id,
        )
        self.assertEqual(
            invoice.delivery_transport_reason_id,
            sale_order.default_transport_reason_id,
        )
        self.assertEqual(
            invoice.delivery_transport_method_id,
            sale_order.default_transport_method_id,
        )
