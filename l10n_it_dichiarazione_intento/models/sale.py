# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def _set_fiscal_position(self):
        for sale in self:
            if sale.partner_id and sale.date_order:
                dichiarazioni = self.env['dichiarazione.intento'].get_valid(
                    'out',
                    sale.partner_id.id,
                    fields.Date.to_date(sale.date_order))
                if dichiarazioni:
                    sale.fiscal_position_id = \
                        dichiarazioni[0].fiscal_position_id.id

    @api.onchange('date_order')
    def onchange_date_order(self):
        self._set_fiscal_position()

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        res = super(SaleOrder, self).onchange_partner_id()
        self._set_fiscal_position()
        return res
