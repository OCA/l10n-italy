#  Copyright 2021 Alfredo Zamora - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _prepare_phantom_move_values(self, bom_line, quantity):
        """
        inherit to change name to product_multiline_description_sale
        """
        ret = super(StockMove, self)._prepare_phantom_move_values(bom_line, quantity)

        ret.update({
            'name': bom_line.product_id.get_product_multiline_description_sale()
        })
        return ret
