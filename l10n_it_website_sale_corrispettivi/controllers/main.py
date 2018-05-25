# -*- coding: utf-8 -*-
# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleCorrispettivi(WebsiteSale):

    def _checkout_form_save(self, mode, checkout, all_values):
        res = super(WebsiteSaleCorrispettivi, self) \
            ._checkout_form_save(mode, checkout, all_values)
        use_invoice = all_values.get('use_invoice')
        order = request.website.sale_get_order()
        order.write({'corrispettivi': not use_invoice})
        return res
