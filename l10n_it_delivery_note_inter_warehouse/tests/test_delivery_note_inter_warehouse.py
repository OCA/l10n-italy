# Copyright 2023 Ooops404
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import SavepointCase
from odoo.tests.common import Form


class TestDeliveryNoteInterWarehouse(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Partner = cls.env["res.partner"]
        cls.Company = cls.env["res.company"]
        cls.Product = cls.env["product.product"]
        cls.StockMove = cls.env["stock.move"]
        cls.StockWarehouse = cls.env["stock.warehouse"]
        cls.StockPicking = cls.env["stock.picking"]
        cls.StockPickingType = cls.env["stock.picking.type"]
        cls.StockDeliveryNote = cls.env["stock.delivery.note"]

        cls.user = cls.env.ref("base.user_admin")

        cls.test_company = cls.Company.create({"name": "Test Company"})
        cls.wh1 = cls.StockWarehouse.search([("company_id", "=", cls.test_company.id)])
        cls.wh2 = cls.StockWarehouse.create(
            {
                "partner_id": cls.test_company.partner_id.id,
                "name": "WH2 Test",
                "code": "WH2T",
                "company_id": cls.test_company.id,
            }
        )
        cls.partner_1 = cls.Partner.create({"name": "WH1"})
        cls.wh1.write(
            {
                "inter_warehouse_transfers": True,
                "receipt_destination_location_id": cls.wh1.lot_stock_id.id,
                "receipt_picking_type_id": cls.wh1.in_type_id.id,
                "receipt_picking_partner_id": cls.partner_1.id,
            }
        )
        cls.partner_2 = cls.Partner.create({"name": "WH2"})
        cls.wh2.write(
            {
                "inter_warehouse_transfers": True,
                "receipt_destination_location_id": cls.wh2.lot_stock_id.id,
                "receipt_picking_type_id": cls.wh2.in_type_id.id,
                "receipt_picking_partner_id": cls.partner_2.id,
            }
        )

        cls.product_oven = cls.Product.create(
            {
                "name": "Microwave Oven",
                "type": "product",
                "standard_price": 1.0,
                "weight": 20,
                "volume": 1.5,
            }
        )
        cls.product_refrigerator = cls.Product.create(
            {
                "name": "Refrigerator",
                "type": "product",
                "standard_price": 1.0,
                "weight": 10,
                "volume": 1,
            }
        )

    def test_inter_company_delivery_note(self):
        self.wh1.int_type_id.write(
            {
                "inter_warehouse_transfer": True,
                "disable_merge_picking_moves": True,
            }
        )

        picking_out = self.StockPicking.create(
            {
                "partner_id": self.partner_2.id,
                "picking_type_id": self.wh1.int_type_id.id,
                "location_id": self.wh1.int_type_id.default_location_src_id.id,
                "location_dest_id": self.partner_2.default_stock_location_src_id.id,
                "move_lines": [
                    (
                        0,
                        0,
                        {
                            "name": self.product_oven.name,
                            "product_id": self.product_oven.id,
                            "product_uom_qty": 3,
                            "product_uom": self.product_oven.uom_id.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": self.product_refrigerator.name,
                            "product_id": self.product_refrigerator.id,
                            "product_uom_qty": 3,
                            "product_uom": self.product_refrigerator.uom_id.id,
                        },
                    ),
                ],
            }
        )

        for ml in picking_out.move_lines:
            ml.quantity_done = 3
        for ml in picking_out.move_lines.move_line_ids:
            ml.qty_done = 3
        picking_out.button_validate()

        dn_out = picking_out.delivery_note_id
        dn_out.action_confirm()
        move_in = self.StockMove.search(
            [("inter_warehouse_picking_id", "=", picking_out.id)]
        )
        picking_in = move_in.picking_id
        for ml in picking_in.move_lines:
            ml.quantity_done = 3
        for ml in picking_in.move_lines.move_line_ids:
            ml.qty_done = 3
        picking_in.button_validate()
        dn_form = Form(
            self.env["stock.delivery.note.create.wizard"].with_context(
                {"active_ids": picking_in.ids}
            )
        )
        dn_in = dn_form.save()
        dn_in.confirm()
        self.assertEqual(picking_in.delivery_note_id.partner_ref, dn_out.name)
