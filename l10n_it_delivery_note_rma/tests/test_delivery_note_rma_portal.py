# Copyright 2023 Nextev

from odoo.tests import Form, SavepointCase
from odoo.tests.common import users


class TestRmaDeliveryNote(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Users = cls.env["res.users"].with_context({"no_reset_password": True})
        group_id = [
            (6, 0, [cls.env.ref("base.group_portal").id]),
        ]
        cls.user_portal = Users.create(
            {
                "name": "Partner test",
                "login": "partner@rma",
                "email": "partner@rma",
                "groups_id": group_id,
            }
        )
        cls.product_product = cls.env["product.product"]
        cls.sale_order = cls.env["sale.order"]

        cls.product_1 = cls.product_product.create(
            {"name": "Product test 1", "type": "product"}
        )
        cls.partner = cls.user_portal.partner_id
        cls._partner_portal_wizard(cls, cls.partner)
        order_form = Form(cls.sale_order)
        order_form.partner_id = cls.partner
        with order_form.order_line.new() as line_form:
            line_form.product_id = cls.product_1
            line_form.product_uom_qty = 5
        cls.sale_order = order_form.save()
        cls.sale_order.action_confirm()
        cls.order_line = cls.sale_order.order_line.filtered(
            lambda r: r.product_id == cls.product_1
        )
        cls.order_out_picking = cls.sale_order.picking_ids
        cls.order_out_picking.move_lines.quantity_done = 5
        cls.order_out_picking.button_validate()

    def _partner_portal_wizard(self, partner):
        wizard_all = (
            self.env["portal.wizard"]
            .with_context({"active_ids": [partner.id]})
            .create({})
        )
        wizard_all.user_ids.in_portal = True
        wizard_all.action_apply()

    @users("partner@rma")
    def test_create_rma_from_ddt_portal_user(self):
        delivery_note = self.sale_order.picking_ids.delivery_note_id
        wizard_obj = self.env["stock.delivery.note.rma.wizard"].sudo()
        wizard_line_obj = self.env["stock.delivery.note.line.rma.wizard"].sudo()
        operation = self.env["rma.operation"].sudo().search([], limit=1)
        wizard_line = wizard_line_obj.sudo().create(
            {
                "delivery_note_id": delivery_note.id,
                "product_id": delivery_note.line_ids[0].product_id.id,
                "quantity": delivery_note.line_ids.product_qty,
                "uom_id": delivery_note.line_ids.product_uom_id.id,
                "picking_id": delivery_note.line_ids.move_id.picking_id.id,
                "operation_id": operation.id,
            }
        )
        wizard = wizard_obj.create(
            {
                "delivery_note_id": delivery_note.id,
                "line_ids": wizard_line,
            }
        )
        rma = wizard.sudo().create_rma()
        self.assertTrue(rma)
        self.assertEqual(rma.partner_id, self.partner)
        self.assertEqual(rma.delivery_note_id, delivery_note)
