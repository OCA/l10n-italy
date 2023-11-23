# Copyright 2023 Ooops404
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import SavepointCase
from odoo.tests.common import Form


class TestDeliveryNoteInterCompany(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.PurchaseOrder = cls.env["purchase.order"]
        cls.SaleOrder = cls.env["sale.order"]
        cls.StockPicking = cls.env["stock.picking"]
        cls.StockDeliveryNote = cls.env["stock.delivery.note"]

        cls.user = cls.env.ref("base.user_admin")

        cls.company_a = cls.env.ref("base.main_company")
        cls.company_b = cls.env.ref("stock.res_company_1")

        cls.company_a.so_from_po = True
        cls.company_a.sync_picking = True
        cls.company_a.warehouse_id = cls.env.ref("stock.warehouse0")
        cls.company_a.intercompany_sale_user_id = cls.user.id

        cls.company_b.so_from_po = True
        cls.company_b.sync_picking = True
        cls.company_b.warehouse_id = cls.env.ref("stock.stock_warehouse_shop0")
        cls.company_b.intercompany_sale_user_id = cls.user.id

        cls.product = cls.env.ref("product.product_product_9")
        cls.purchase_order = cls.PurchaseOrder.create(
            {
                "company_id": cls.company_a.id,
                "partner_id": cls.company_b.partner_id.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": cls.product.name,
                            "product_id": cls.product.id,
                            "product_qty": 5.0,
                            "product_uom": cls.product.uom_po_id.id,
                            "price_unit": 10.0,
                        },
                    ),
                ],
            }
        )

    def test_inter_company_delivery_note(self):
        """
        Test the main flow of this module

        - Create and approve purchase order
        - Relative sale order must be created
        - Approve the picking of the sale order
        - Automatically, the relative picking of the
            purchase order must be approved too
        - Check that the partner_ref of the purchase
            order is equal to the name of the sale_order
        - Check that every relevant field is synced
            between the two delivery notes
        """

        self.purchase_order.button_approve()
        sale_order = self.SaleOrder.search(
            [("auto_purchase_order_id", "=", self.purchase_order.id)]
        )
        self.assertTrue(sale_order)

        po_picking_id = self.purchase_order.picking_ids
        so_picking_id = sale_order.picking_ids

        so_picking_id.move_lines.quantity_done = 2
        so_picking_id.state = "done"
        wizard_data = so_picking_id.button_validate()
        wizard = (
            self.env["stock.backorder.confirmation"]
            .with_context(**wizard_data.get("context"))
            .create({})
        )
        wizard.process()

        self.assertEqual(
            po_picking_id.move_lines.quantity_done,
            so_picking_id.move_lines.quantity_done,
        )

        dn_form = Form(
            self.env["stock.delivery.note.create.wizard"].with_context(
                {"active_ids": po_picking_id.ids}
            )
        )
        dn = dn_form.save()
        dn.confirm()

        self.assertTrue(po_picking_id.delivery_note_id)
        self.assertEqual(
            po_picking_id.delivery_note_id.partner_ref,
            so_picking_id.delivery_note_id.name,
        )

        so_picking_id.delivery_note_id.update_detail_lines()
        sync_fields = self.StockDeliveryNote._get_sync_fields()
        for i in sync_fields:
            self.assertEqual(
                so_picking_id.delivery_note_id[i], po_picking_id.delivery_note_id[i]
            )
