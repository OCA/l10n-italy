# -*- coding: utf-8 -*-
# Copyright 2016 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models, _
from openerp.exceptions import Warning as UserError


class DdtFromPickings(models.TransientModel):

    _inherit = 'ddt.from.pickings'

    @api.multi
    def create_ddt(self):
        self.ensure_one()
        res = super(DdtFromPickings, self).create_ddt()
        carriers = self.mapped('picking_ids.carrier_id')
        if len(carriers) > 1:
            raise UserError(_("Selected Pickings have different carriers"))
        ddt = self.env['stock.picking.package.preparation'].browse(
            res['res_id'])
        # get carrier from the picking's delivery carrier
        ddt.carrier_id = carriers.partner_id.id
        return res
