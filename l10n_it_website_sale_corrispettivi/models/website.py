# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class Website(models.Model):
    _inherit = 'website'

    @api.multi
    def _prepare_sale_order_values(self, partner, pricelist):
        self.ensure_one()
        values = super(Website, self) \
            ._prepare_sale_order_values(partner, pricelist)
        values.update({'corrispettivi': partner.use_corrispettivi})
        return values
