# Copyright (C) 2023-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Marco Calcagni <mcalcagni@dinamicheaziendali.it>
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# Copyright 2024 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.tools import float_compare


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_purchase_price_unit(self):
        """Unit price of the purchase line, in company currency and product UoM.

        It is the average price of the posted bills of the purchase line, net of
        the posted refunds, or the purchase price if nothing is invoiced yet.
        """
        self.ensure_one()
        purchase_line = self.purchase_line_id
        StockMoveLine = self.env["stock.move.line"]
        invoiced_amount, invoiced_qty = StockMoveLine._get_invoiced_amount_qty(
            purchase_line
        )
        rounding = purchase_line.product_id.uom_id.rounding
        if float_compare(invoiced_qty, 0, precision_rounding=rounding) > 0:
            return invoiced_amount / invoiced_qty
        purchase = purchase_line.order_id
        price_subtotal = purchase.currency_id._convert(
            purchase_line.price_subtotal,
            purchase.company_id.currency_id,
            purchase.company_id,
            purchase.date_order or fields.Date.today(),
        )
        return price_subtotal / (purchase_line.product_uom_qty or 1)
