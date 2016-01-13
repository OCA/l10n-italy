# -*- coding: utf-8 -*-
# © 2016 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp import models, fields, api


class StockPickingPackagePreparationLine(models.Model):

    _inherit = 'stock.picking.package.preparation.line'
    product_customer_code = fields.Char(
        'Product Customer Code', compute='_compute_customer_code')

    @api.one
    def _compute_customer_code(self):
        code = u''
        if self.move_id and self.move_id.product_customer_code:
            code = self.move_id.product_customer_code
        self.product_customer_code = code
