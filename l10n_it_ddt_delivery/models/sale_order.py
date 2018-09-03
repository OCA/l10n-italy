# Copyright 2016 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def _preparare_ddt_data(self):
        res = super(SaleOrder, self)._preparare_ddt_data()
        self.ensure_one()
        # get carrier from the sale order's delivery carrier
        res.update({'carrier_id': self.ddt_carrier_id.id})
        return res
