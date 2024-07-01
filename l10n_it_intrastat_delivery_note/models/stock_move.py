from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _get_aggregated_product_quantities(self, **kwargs):
        aggregated_move_lines = super()._get_aggregated_product_quantities(**kwargs)
        for aggregated_move_line in aggregated_move_lines:
            intrastat_code = aggregated_move_lines[aggregated_move_line][
                "product"
            ].product_tmpl_id.intrastat_code_id.name
            aggregated_move_lines[aggregated_move_line][
                "intrastat_code_id"
            ] = intrastat_code
        return aggregated_move_lines
