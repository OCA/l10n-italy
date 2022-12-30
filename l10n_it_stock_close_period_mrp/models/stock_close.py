# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _
from odoo.exceptions import UserError
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class StockClosePeriodInherit(models.Model):
    _inherit = "stock.close.period"

    force_standard_price = fields.Boolean(
        default=False,
        help="Forces the use of the standard price instead of calculating the cost from the BOM.")
    production_ok = fields.Boolean(
        default=False,
        readonly=True,
        help="Marks if action 'Compute Production' is processed.")

    def action_set_to_draft(self):
        res = super(StockClosePeriodInherit, self).action_set_to_draft()
        self.production_ok = False
        return res

    def action_recalculate_production(self):
        for stock_close in self:
            if not stock_close._check_qty_available():
                raise UserError(_("Is not possible continue the execution. There are product with quantities < 0."))

            stock_close.env["stock.move.line"].recompute_average_cost_period_production()
            stock_close.production_ok = True
            if stock_close.force_archive:
                stock_close._deactivate_moves()
            stock_close.work_end = datetime.now()
        return True


class StockClosePeriodLineInherit(models.Model):
    _inherit = "stock.close.period.line"

    evaluation_method = fields.Selection(selection_add=[("production", "Production")])
