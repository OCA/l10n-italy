# -*- coding: utf-8 -*-
# Copyright 2016 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.model
    def _preparare_ddt_data(self, order):
        res = super(SaleOrder, self)._preparare_ddt_data(order)
        # get carrier from the sale order's delivery carrier
        res.update({'carrier_id': order.carrier_id.partner_id.id})
        return res
