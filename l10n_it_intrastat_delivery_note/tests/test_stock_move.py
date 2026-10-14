from odoo.tests import Form
from odoo.tests.common import TransactionCase


class TestStockMove(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ProductTemplate = cls.env["product.template"]

        cls.partner = cls.env.ref("base.partner_admin")
        cls.stock_location = cls.env.ref("stock.stock_location_stock")
        cls.customer_location = cls.env.ref("stock.stock_location_customers")
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.product = cls.ProductTemplate.search(
            [("intrastat_code_id", "!=", False)]
        ).product_variant_ids[:1]

    def test_move_lines_aggregated(self):
        self.assertEqual(len(self.product), 1)
        self.env["stock.quant"]._update_available_quantity(
            self.product, self.stock_location, 25
        )
        picking = self.env["stock.picking"].create(
            {
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
                "picking_type_id": self.env.ref("stock.picking_type_out").id,
            }
        )
        move1 = self.env["stock.move"].create(
            {
                "name": "test_transit_1",
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
                "product_id": self.product.id,
                "product_uom": self.uom_unit.id,
                "product_uom_qty": 15.0,
                "picking_id": picking.id,
                "picking_type_id": self.env.ref("stock.picking_type_out").id,
            }
        )
        move1.quantity_done = 5
        picking.action_put_in_pack()

        with Form(picking) as delivery_form:
            delivery_form.partner_id = self.partner
            delivery_form.save()

        aggregate_values = picking.move_line_ids._get_aggregated_product_quantities()
        self.assertTrue(bool(aggregate_values))
        for v in aggregate_values.values():
            self.assertEqual(
                v["product"].product_tmpl_id.intrastat_code_id.name,
                v["intrastat_code"],
            )
