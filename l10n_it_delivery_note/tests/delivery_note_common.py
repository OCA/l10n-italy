from odoo.tests.common import TransactionCase

DOWNPAYMENT_METHODS = ["fixed", "percentage"]


class StockDeliveryNoteCommon(TransactionCase):
    def create_partner(self, name, **kwargs):
        return self.env["res.partner"].create({"name": name, **kwargs})

    def create_sales_order(self, lines, **kwargs):
        vals = {"partner_id": self.recipient.id}

        if lines:
            vals["order_line"] = lines

        vals.update(kwargs)

        return self.env["sale.order"].create(vals)

    def prepare_sales_order_line(self, product, quantity=1.0, price=None, **kwargs):
        vals = {"product_id": product.id, "product_uom_qty": quantity}

        if price:
            vals["price_unit"] = price

        vals.update(kwargs)

        return 0, False, vals

    def add_downpayment_line(self, sales_order, method, amount, **kwargs):
        if method not in DOWNPAYMENT_METHODS:
            raise ValueError("Downpayment method must be 'fixed' or 'percentage'.")

        return (
            self.env["sale.advance.payment.inv"]
            .with_context(active_ids=sales_order.ids)
            .create({"advance_payment_method": method, "amount": amount, **kwargs})
            .create_invoices()
        )

    def create_delivery_note(self, **kwargs):
        vals = {
            "partner_sender_id": self.sender.id,
            "partner_id": self.recipient.id,
            "partner_shipping_id": self.recipient.id,
        }

        vals.update(kwargs)

        return self.env["stock.delivery.note"].create(vals)

    def setUp(self):
        super().setUp()

        self.env.user.write(
            {
                "groups_id": [
                    (
                        4,
                        self.env.ref(
                            "l10n_it_delivery_note.use_advanced_delivery_notes"
                        ).id,
                    )
                ]
            }
        )

        self.sender = self.env.ref("base.main_partner")
        self.recipient = self.create_partner("Mario Rossi")

        try:
            self.desk_combination_line = self.prepare_sales_order_line(
                self.env.ref("product.product_product_3"), 1
            )
            self.customizable_desk_line = self.prepare_sales_order_line(
                self.env.ref("product.product_product_4"), 3
            )
            self.right_corner_desk_line = self.prepare_sales_order_line(
                self.env.ref("product.product_product_5"), 2
            )
            self.large_cabinet_line = self.prepare_sales_order_line(
                self.env.ref("product.product_product_6"), 11
            )
            self.storage_box_line = self.prepare_sales_order_line(
                self.env.ref("product.product_product_7"), 5
            )
            self.large_desk_line = self.prepare_sales_order_line(
                self.env.ref("product.product_product_8"), 1
            )

        except ValueError as exc:
            raise RuntimeError(
                "It seems you're not using a database with"
                " demonstration data loaded for this tests."
            ) from exc
