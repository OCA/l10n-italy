#  Copyright 2021 Alfredo Zamora - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def get_mrp_bom(self):
        self.ensure_one()
        return self.env['mrp.bom']._bom_find(
            product=self.product_id,
            company_id=self.company_id.id)
