# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import HttpCase


class TestFrontend(HttpCase):

    def setUp(self):
        super().setUp()
        self.admin_partner = self.env.ref('base.partner_root')

    def test_admin_no_corrispettivi(self):
        """
        If a partner having the flag 'corrispettivi' set to False
        creates an order in frontend, then
        the created order's flag corrispettivi is False"""
        self.assertFalse(self.admin_partner.use_corrispettivi)
        existing_orders = self.env['sale.order'].search([])
        # In frontend, create an order with flag corrispettivi
        self.phantom_js(
            "/",
            "odoo.__DEBUG__.services['web_tour.tour']"
            ".run('shop_buy_product')",
            "odoo.__DEBUG__.services['web_tour.tour']"
            ".tours.shop_buy_product.ready",
            login="admin")
        created_order = self.env['sale.order'].search([
            ('id', 'not in', existing_orders.ids)])
        self.assertFalse(created_order.corrispettivi)
