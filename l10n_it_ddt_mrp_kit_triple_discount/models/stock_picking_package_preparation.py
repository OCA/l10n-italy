#  Copyright 2021 Alfredo Zamora - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, api


class StockPickingPackagePreparationLine(models.Model):
    _inherit = "stock.picking.package.preparation.line"

    @api.multi
    def _prepare_invoice_line(self, qty, invoice_id=None):
        res = super(StockPickingPackagePreparationLine, self)._prepare_invoice_line(
            qty,
            invoice_id
        )

        mrp_bom = self.sale_line_id.get_mrp_bom()

        if mrp_bom:
            res.update({
                'discount2': False,
                'discount3': False,
            })
        return res
