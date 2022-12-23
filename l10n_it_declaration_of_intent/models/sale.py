# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def _set_fiscal_position(self):
        for sale in self:
            if sale.partner_id and sale.date_order:
                declarations = self.env[
                    "l10n_it_declaration_of_intent.declaration"
                ].get_valid(
                    "out", sale.partner_id.id, fields.Date.to_date(sale.date_order)
                )
                if declarations:
                    sale.fiscal_position_id = declarations[0].fiscal_position_id.id

    @api.onchange("date_order")
    def onchange_date_order(self):
        self._set_fiscal_position()

    def _compute_fiscal_position_id(self):
        res = super()._compute_fiscal_position_id()
        self._set_fiscal_position()
        return res
