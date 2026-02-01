#  Copyright 2023 Simone Rubino - Aion Tech
#  Copyright 2025 Simone Rubino
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.fields import Command
from odoo.tests import Form, tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


def _init_sale_order(env, partner, products):
    group_sale_manger = env.ref("sales_team.group_sale_manager")
    env.user.write({"group_ids": [Command.link(group_sale_manger.id)]})

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
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
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
        cls.product = cls.env["product.product"].create(
            {
                "name": "Drawer Black",
                "list_price": 25.0,
                "type": "consu",
                "default_code": "FURN_8900",
            }
        )
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
            "l10n_it_delivery_note.transport_condition_PF"
        )
        sale_order.default_goods_appearance_id = self.env.ref(
            "l10n_it_delivery_note.goods_appearance_CAR"
        )
        sale_order.default_transport_reason_id = self.env.ref(
            "l10n_it_delivery_note.transport_reason_VEN"
        )
        sale_order.default_transport_method_id = self.env.ref(
            "l10n_it_delivery_note.transport_method_MIT"
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
