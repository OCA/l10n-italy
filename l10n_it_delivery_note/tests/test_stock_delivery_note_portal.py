# Copyright 2023 Nextev Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import AccessError
from odoo.tests import Form, HttpCase, new_test_user

from .delivery_note_common import StockDeliveryNoteCommon


class StockDeliveryNotePortal(StockDeliveryNoteCommon, HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user_mr = new_test_user(
            cls.env,
            login="mr",
            password="portal",
            groups="base.group_portal",
        )
        cls.user_mr.partner_id = cls.recipient

        # Mario Rossi SO
        cls.sales_order_mr = cls.create_sales_order(
            [
                cls.large_desk_line,  # 1
                cls.desk_combination_line,  # 1
            ],
        )
        cls.sales_order_mr.action_confirm()
        cls.picking_mr = cls.sales_order_mr.picking_ids

        cls.picking_mr.move_ids.quantity = False
        cls.picking_mr.move_ids[0].quantity = 1
        cls.picking_mr.move_ids[1].quantity = 1

        cls.picking_mr.button_validate()
        dn = Form.from_action(
            cls.env, cls.picking_mr.action_delivery_note_create()
        ).save()
        dn.confirm()
        cls.delivery_note_mr = cls.picking_mr.delivery_note_id
        cls.delivery_note_mr.action_confirm()

        # Anna Bianchi SO
        company_ab = cls.create_commercial_partner("Azienda Bianchi")
        anna_bianchi = cls.create_partner("Anna Bianchi", company_ab)
        cls.recipient = anna_bianchi
        cls.sales_order_ab = cls.create_sales_order(
            [
                cls.desk_combination_line,  # 1
                cls.customizable_desk_line,  # 3
            ],
        )
        cls.sales_order_ab.action_confirm()
        cls.picking_ab = cls.sales_order_ab.picking_ids

        cls.picking_ab.move_ids.quantity = False
        cls.picking_ab.move_ids[0].quantity = 1
        cls.picking_ab.move_ids[1].quantity = 3

        cls.picking_ab.button_validate()
        dn = Form.from_action(
            cls.env, cls.picking_ab.action_delivery_note_create()
        ).save()
        dn.confirm()
        cls.delivery_note_ab = cls.picking_ab.delivery_note_id
        cls.delivery_note_ab.action_confirm()

        # Anna Bianchi fatturazione, Mario Rossi spedizione
        cls.sales_order_ab_mr = cls.create_sales_order(
            [
                cls.large_desk_line,  # 1
            ],
        )
        cls.sales_order_ab_mr.action_confirm()
        cls.picking_ab_mr = cls.sales_order_ab_mr.picking_ids
        cls.picking_ab_mr.partner_id = cls.user_mr.partner_id

        cls.picking_ab_mr.move_ids.quantity = False
        cls.picking_ab_mr.move_ids[0].quantity = 1

        cls.picking_ab_mr.button_validate()
        dn = Form.from_action(
            cls.env, cls.picking_ab_mr.action_delivery_note_create()
        ).save()
        dn.confirm()
        cls.delivery_note_ab_mr = cls.picking_ab_mr.delivery_note_id
        cls.delivery_note_ab_mr.action_confirm()

        # Azienda Rossi SO
        cls.recipient = cls.user_mr.partner_id.parent_id
        cls.sales_order_azr = cls.create_sales_order(
            [
                cls.desk_combination_line,  # 1
            ],
        )
        cls.sales_order_azr.action_confirm()
        cls.picking_azr = cls.sales_order_azr.picking_ids

        cls.picking_azr.move_ids.quantity = False
        cls.picking_azr.move_ids[0].quantity = 1

        cls.picking_azr.button_validate()
        dn = Form.from_action(
            cls.env, cls.picking_azr.action_delivery_note_create()
        ).save()
        dn.confirm()
        cls.delivery_note_azr = cls.picking_azr.delivery_note_id
        cls.delivery_note_azr.action_confirm()

    def test_access_portal_user(self):
        """Test portal user's access rights"""
        # Portal users can see the Delivery Notes for which they
        # are assigned as recipient or delivery address
        self.assertTrue(
            self.delivery_note_mr.with_user(self.user_mr).has_access("read")
        )

        # Portal users can't edit the DN
        with self.assertRaises(AccessError):
            self.delivery_note_mr.with_user(self.user_mr).write({"packages": 1})
        # Portal users can't create the DN
        with self.assertRaises(AccessError):
            self.env["stock.delivery.note"].with_user(self.user_mr).create({})
        # Portal users can't delete the DN
        with self.assertRaises(AccessError):
            self.delivery_note_mr.with_user(self.user_mr).action_cancel()
        with self.assertRaises(AccessError):
            self.delivery_note_mr.with_user(self.user_mr).unlink()

        # Portal users can't see the Delivery Notes for which they
        # aren't assigned as recipient or delivery address
        self.assertFalse(
            self.delivery_note_ab.with_user(self.user_mr).has_access("read")
        )

        # Portal users can't edit the DN
        with self.assertRaises(AccessError):
            self.delivery_note_ab.with_user(self.user_mr).write({"packages": 1})
        # Portal users can't delete the DN
        with self.assertRaises(AccessError):
            self.delivery_note_ab.with_user(self.user_mr).action_cancel()
        with self.assertRaises(AccessError):
            self.delivery_note_ab.with_user(self.user_mr).unlink()

        # Portal users can see the Delivery Notes for which they
        # are assigned as delivery address
        self.assertTrue(
            self.delivery_note_ab_mr.with_user(self.user_mr).has_access("read")
        )

        # Portal users can't edit the DN
        with self.assertRaises(AccessError):
            self.delivery_note_ab_mr.with_user(self.user_mr).write({"packages": 1})
        # Portal users can't delete the DN
        with self.assertRaises(AccessError):
            self.delivery_note_ab_mr.with_user(self.user_mr).action_cancel()
        with self.assertRaises(AccessError):
            self.delivery_note_ab_mr.with_user(self.user_mr).unlink()

        # Portal users can see the Delivery Notes for which their company
        # are assigned as recipient
        self.assertTrue(
            self.delivery_note_azr.with_user(self.user_mr).has_access("read")
        )

        # Portal users can't edit the DN
        with self.assertRaises(AccessError):
            self.delivery_note_azr.with_user(self.user_mr).write({"packages": 1})
        # Portal users can't delete the DN
        with self.assertRaises(AccessError):
            self.delivery_note_azr.with_user(self.user_mr).action_cancel()
        with self.assertRaises(AccessError):
            self.delivery_note_azr.with_user(self.user_mr).unlink()

    def test_access_myportal_user(self):
        """Test portal user DN urls access in its portal"""
        base_url = "/my/delivery-notes/"
        url_delivery_note_mr = f"{base_url}{self.delivery_note_mr.id}"
        url_delivery_note_ab = f"{base_url}{self.delivery_note_ab.id}"
        url_delivery_note_ab_mr = f"{base_url}{self.delivery_note_ab_mr.id}"
        url_delivery_note_azr = f"{base_url}{self.delivery_note_azr.id}"

        # Authenticate with Mario Rossi
        self.authenticate("mr", "portal")
        # User can access Delivery Notes for which it's assigned as recipient
        self.assertEqual(
            self.url_open(url=url_delivery_note_mr).request.path_url,
            url_delivery_note_mr,
        )
        # User can't access Delivery Notes for which it isn't assigned
        # as recipient or delivery address and it will be redirected to "my" page
        self.assertEqual(
            self.url_open(url=url_delivery_note_ab).request.path_url, "/my"
        )
        # User can access Delivery Notes for which it's assigned as delivery address
        self.assertEqual(
            self.url_open(url=url_delivery_note_ab_mr).request.path_url,
            url_delivery_note_ab_mr,
        )
        # User can access Delivery Notes for which its company is assigned
        # as recipient
        self.assertEqual(
            self.url_open(url=url_delivery_note_azr).request.path_url,
            url_delivery_note_azr,
        )
