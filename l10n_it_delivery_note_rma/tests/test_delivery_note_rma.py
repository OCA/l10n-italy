from odoo.exceptions import ValidationError
from odoo.tests import new_test_user
from odoo.tests.common import Form

from .delivery_note_common import StockDeliveryNoteCommon


class TestDeliveryNoteRma(StockDeliveryNoteCommon):
    def setUp(self):
        super().setUp()
        user = new_test_user(
            self.env,
            login="test",
            groups="stock.group_stock_manager,"
            "l10n_it_delivery_note.use_advanced_delivery_notes",
        )
        # change user in order to automatically create delivery note
        # when picking is validated
        self.env.user = user
        picking = self.env["stock.picking"].create(
            {
                "partner_id": self.recipient.id,
                "picking_type_id": self.env.ref("stock.picking_type_out").id,
                "location_id": self.env.ref("stock.stock_location_stock").id,
                "location_dest_id": self.env.ref("stock.stock_location_customers").id,
            }
        )
        self.picking = picking
        self.env["stock.move"].create(
            {
                "name": self.env.ref("product.product_product_8").name,
                "product_id": self.env.ref("product.product_product_8").id,
                "product_uom_qty": 1,
                "product_uom": self.env.ref("product.product_product_8").uom_id.id,
                "picking_id": picking.id,
                "location_id": self.env.ref("stock.stock_location_stock").id,
                "location_dest_id": self.env.ref("stock.stock_location_customers").id,
            }
        )

        # deliver product
        picking.move_lines.quantity_done = 1
        picking.button_validate()

        # create delivery note with advanced mode
        dn_form = Form(
            self.env["stock.delivery.note.create.wizard"].with_context(
                {"active_ids": [picking.id]}
            )
        )
        dn = dn_form.save()
        dn.confirm()

        self.assertRaises(ValidationError, picking.delivery_note_id.action_create_rma)
        picking.delivery_note_id.action_confirm()
        self.delivery_note = picking.delivery_note_id
        self.delivery_note_line = self.delivery_note.line_ids[0]
        self.product_product = self.env["product.product"]

        self.product_1 = self.product_product.create(
            {"name": "Product test 1", "type": "product"}
        )

    def test_create_rma_with_dn(self):
        rma_form = Form(self.env["rma"])
        rma_form.partner_id = self.recipient
        rma_form.delivery_note_id = self.delivery_note
        rma_form.product_id = self.product_1
        rma_form.product_uom_qty = 5
        rma_form.location_id = self.delivery_note.warehouse_id.rma_loc_id
        rma = rma_form.save()
        rma.action_confirm()
        self.assertTrue(rma.reception_move_id, msg="Move_id must not be empty")
        self.assertFalse(
            rma.reception_move_id.origin_returned_move_id,
            msg="returned_move_id must be false",
        )

    def test_create_rma_from_dn(self):
        delivery_note = self.delivery_note
        wizard_id = delivery_note.action_create_rma()["res_id"]
        wizard = self.env["stock.delivery.note.rma.wizard"].browse(wizard_id)
        rma = self.env["rma"].browse(wizard.create_and_open_rma()["res_id"])
        self.assertEqual(
            rma.partner_id,
            delivery_note.partner_id,
            msg="partner_id must be taken from dn",
        )
        self.assertEqual(
            rma.delivery_note_id,
            delivery_note,
            msg="delivery_note_id must be equal created dn",
        )
        self.assertEqual(
            rma.picking_id, self.picking, msg="picking_id must be equal creted picking"
        )
        self.assertEqual(
            rma.move_id,
            self.picking.move_lines,
            msg="move_id must be equal created stock.move",
        )
        self.assertEqual(
            rma.product_id,
            self.delivery_note_line.product_id,
            msg="product must be equal to dn line product",
        )
        self.assertEqual(
            rma.product_uom_qty,
            self.delivery_note_line.product_qty,
            msg="product qty must be equal to dn line product qty",
        )
        self.assertEqual(
            rma.product_uom,
            self.delivery_note_line.product_uom_id,
            msg="product uom must be equal to dn line product uom id",
        )
        self.assertEqual(rma.state, "draft", msg="state must be equal to draft")
        self.assertEqual(
            delivery_note.rma_count, 1, msg="must be equal to number of created rma"
        )
        self.assertEqual(
            rma.reception_move_id.picking_id + self.picking,
            delivery_note.picking_ids,
            msg="""sum of created picking and picking from reception move
            must be equal to dn picking""",
        )
        rma.action_confirm()
        self.assertEqual(rma.state, "confirmed", msg="state must be confirmed")
        self.assertEqual(
            rma.reception_move_id.origin_returned_move_id,
            self.picking.move_lines,
            msg="returned move from rma must be equal to picking.move_lines",
        )

        action = self.env["ir.actions.act_window"]._for_xml_id("rma.rma_action")
        action.update(
            res_id=rma.id,
            view_mode="form",
            views=[],
        )
        action["context"] = {}

        action_from_dn = delivery_note.action_view_rma()

        self.assertEqual(action, action_from_dn, "Must be created action in form type")

        self.env["rma"].browse(wizard.create_and_open_rma()["res_id"])
        action_for_list = self.env["ir.actions.act_window"]._for_xml_id(
            "rma.rma_action"
        )
        action_for_list["domain"] = [("id", "in", delivery_note.rma_ids.ids)]
        action_for_list["context"] = {}
        self.assertEqual(
            action_for_list, delivery_note.action_view_rma(), "Must be in list view"
        )

        # Refund the RMA
        rma.reception_move_id.quantity_done = rma.product_uom_qty
        rma.reception_move_id.picking_id._action_done()
        rma.action_refund()
        self.assertEqual(
            rma.refund_id.partner_id,
            delivery_note.partner_id,
            msg="partned_id from refund must be equal to partner_id from dn",
        )

    def test_create_rma_from_dn_with_delivery_address(self):
        delivery_address = self.env["res.partner"].create(
            {
                "company_type": "person",
                "firstname": "Delivery",
                "lastname": "Address",
                "type": "delivery",
                "parent_id": self.recipient.id,
            }
        )
        delivery_note = self.delivery_note
        wizard_id = delivery_note.action_create_rma()["res_id"]
        wizard = self.env["stock.delivery.note.rma.wizard"].browse(wizard_id)
        rma = self.env["rma"].browse(wizard.create_and_open_rma()["res_id"])
        self.assertEqual(
            rma.partner_shipping_id,
            delivery_address,
            msg="rma shipping address must be equal to partner delivery address",
        )

    def test_create_rma_from_dn_with_invoice_address(self):
        invoice_address = self.env["res.partner"].create(
            {
                "company_type": "person",
                "firstname": "Invoice",
                "lastname": "Address",
                "type": "invoice",
                "parent_id": self.recipient.id,
            }
        )
        delivery_note = self.delivery_note
        wizard_id = delivery_note.action_create_rma()["res_id"]
        wizard = self.env["stock.delivery.note.rma.wizard"].browse(wizard_id)
        rma = self.env["rma"].browse(wizard.create_and_open_rma()["res_id"])
        self.assertEqual(
            rma.partner_invoice_id,
            invoice_address,
            msg="rma invoice address must be equal to partner invoice address",
        )

    def test_create_rma_from_dn_with_delivery_invoice_address(self):
        delivery_address = self.env["res.partner"].create(
            {
                "company_type": "person",
                "firstname": "Delivery",
                "lastname": "Address",
                "type": "delivery",
                "parent_id": self.recipient.id,
            }
        )
        invoice_address = self.env["res.partner"].create(
            {
                "company_type": "person",
                "firstname": "Invoice",
                "lastname": "Address",
                "type": "invoice",
                "parent_id": self.recipient.id,
            }
        )
        delivery_note = self.delivery_note
        wizard_id = delivery_note.action_create_rma()["res_id"]
        wizard = self.env["stock.delivery.note.rma.wizard"].browse(wizard_id)
        rma = self.env["rma"].browse(wizard.create_and_open_rma()["res_id"])
        self.assertEqual(
            rma.partner_shipping_id,
            delivery_address,
            msg="rma shipping address must be equal to partner delivery address",
        )
        self.assertEqual(
            rma.partner_invoice_id,
            invoice_address,
            msg="rma invoice address must be equal to partner invoice address",
        )

    def test_create_rma_from_dn_with_so(self):
        sales_order = self.create_sales_order(self.desk_combination_line)

        sales_order.action_confirm()

        picking = sales_order.picking_ids
        picking.move_lines[0].quantity_done = 1
        picking.button_validate()

        dn_form = Form(
            self.env["stock.delivery.note.create.wizard"].with_context(
                {"active_ids": [picking.id]}
            )
        )
        dn = dn_form.save()
        dn.confirm()

        picking.delivery_note_id.action_confirm()

        delivery_note = picking.delivery_note_id
        wizard_id = delivery_note.action_create_rma()["res_id"]
        wizard = self.env["stock.delivery.note.rma.wizard"].browse(wizard_id)
        rma = self.env["rma"].browse(wizard.create_and_open_rma()["res_id"])
        self.assertEqual(
            rma.partner_id,
            delivery_note.sale_ids[0].partner_id,
            msg="""partner_id from rma must be equal to
            partner_id from sale_order linked with dn""",
        )
