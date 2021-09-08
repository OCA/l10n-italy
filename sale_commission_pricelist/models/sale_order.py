# Copyright 2018 Tecnativa - Carlos Dauden <carlos.dauden@tecnativa.com>
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_commission_from_pricelist(self):
        self.ensure_one()
        if not self.product_id or not self.order_id.pricelist_id:
            return False  # pragma: no cover
        rule_id = self.order_id.pricelist_id.get_product_price_rule(
            product=self.product_id,
            quantity=self.product_uom_qty or 1.0,
            partner=self.order_id.partner_id,
            date=self.order_id.date_order,
            uom_id=self.product_uom.id,
        )[1]
        rule = self.env["product.pricelist.item"].browse(rule_id)
        return rule.commission_id

    @api.depends("order_id.pricelist_id")
    def _compute_agent_ids(self):
        super(SaleOrderLine, self)._compute_agent_ids()
        for record in self:
            commission = record._get_commission_from_pricelist()
            if record.agent_ids and commission:
                record.agent_ids.update({"commission_id": commission.id})

    def _prepare_agent_vals(self, agent):
        self.ensure_one()
        res = super(SaleOrderLine, self)._prepare_agent_vals(agent)
        commission = self._get_commission_from_pricelist()
        if commission:
            res["commission_id"] = commission.id
        return res
