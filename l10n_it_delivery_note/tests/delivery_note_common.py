from odoo.tests.common import TransactionCase

from odoo.addons.mail.tests.common import mail_new_test_user

DOWNPAYMENT_METHODS = ["fixed", "percentage"]


class StockDeliveryNoteCommon(TransactionCase):
    def create_commercial_partner(self, name, **kwargs):
        return self.env["res.partner"].create(
            {"name": name, "is_company": True, **kwargs}
        )

    def create_partner(self, name, company, **kwargs):
        return self.env["res.partner"].create(
            {"name": name, "parent_id": company.id, **kwargs}
        )

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

    def create_picking(self, **kwargs):
        picking_data = {
            "partner_id": self.recipient.id,
            "picking_type_id": self.env.ref("stock.picking_type_out").id,
            "location_id": self.env.ref("stock.stock_location_stock").id,
            "location_dest_id": self.env.ref("stock.stock_location_customers").id,
            "move_ids": [
                (
                    0,
                    0,
                    {
                        "name": self.env.ref("product.product_product_8").name,
                        "product_id": self.env.ref("product.product_product_8").id,
                        "product_uom_qty": 1,
                        "product_uom": self.env.ref(
                            "product.product_product_8"
                        ).uom_id.id,
                        "location_id": self.env.ref("stock.stock_location_stock").id,
                        "location_dest_id": self.env.ref(
                            "stock.stock_location_customers"
                        ).id,
                    },
                )
            ],
        }

        picking_data.update(kwargs)

        return self.env["stock.picking"].create(picking_data)

    def setUp(self):
        super().setUp()

        self.account_manager = mail_new_test_user(
            self.env,
            name="Adviser",
            login="fm",
            email="accountmanager@yourcompany.com",
            groups="account.group_account_manager,base.group_partner_manager,"
            "base.group_system,sales_team.group_sale_manager,stock.group_stock_manager",
            company_ids=[(6, 0, [c.id for c in self.env["res.company"].search([])])],
        )

        self.sender = self.env.ref("base.main_partner")
        company = self.create_commercial_partner("Azienda Rossi")
        self.recipient = self.create_partner("Mario Rossi", company)

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
