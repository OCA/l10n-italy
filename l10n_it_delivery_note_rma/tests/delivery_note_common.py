from odoo.tests import Form
from odoo.tests.common import TransactionCase

DOWNPAYMENT_METHODS = ["fixed", "percentage"]


class StockDeliveryNoteCommon(TransactionCase):
    def create_partner(self, name, **kwargs):
        return self.env["res.partner"].create({"name": name, **kwargs})

    def create_sales_order(self, line):

        so = self.env["sale.order"].create({"partner_id": self.recipient.id})

        product_product = self.env["product.product"]

        so_product = product_product.create(
            {"name": "Product test 1", "type": "product"}
        )

        with Form(so) as so_form:
            with so_form.order_line.new() as so_form_line:
                so_form_line.product_id = so_product
                so_form_line.product_uom_qty = line.get("product_uom_qty")
            so_form.save()
        return so

    def prepare_sales_order_line(self, product, quantity=1.0, **kwargs):
        vals = {"product_id": product.id, "product_uom_qty": quantity}

        vals.update(kwargs)

        return vals

    def setUp(self):
        super().setUp()

        self.env.ref("l10n_it_delivery_note_base.delivery_note_type_ddt").write(
            {
                "default_transport_condition_id": self.env.ref(
                    "l10n_it_delivery_note_base.transport_condition_PF"
                ),
                "default_goods_appearance_id": self.env.ref(
                    "l10n_it_delivery_note_base.goods_appearance_BAN"
                ),
                "default_transport_reason_id": self.env.ref(
                    "l10n_it_delivery_note_base.transport_reason_VEN"
                ),
                "default_transport_method_id": self.env.ref(
                    "l10n_it_delivery_note_base.transport_method_MIT"
                ),
            }
        )

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

        self.desk_combination_line = self.prepare_sales_order_line(
            self.env.ref("product.product_product_3"), 1
        )
