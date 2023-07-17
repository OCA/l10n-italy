#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class StockPickingPackagePreparationLine(models.Model):
    _inherit = "stock.picking.package.preparation.line"

    @api.multi
    def allow_invoice_line(self):
        self.ensure_one()
        res = super().allow_invoice_line()
        product = self.sale_line_id.product_id
        bom_model = self.env['mrp.bom']
        bom = bom_model._bom_find(product=product) or bom_model.browse()
        is_kit = bom.type == 'phantom'
        return res and not is_kit
