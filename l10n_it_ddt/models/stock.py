# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Apulia Software s.r.l. (http://www.apuliasoftware.it)
#    @author Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
#    Copyright 2015 Lorenzo Battistini - Agile Business Group
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp import fields, models, api


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    ddt_ids = fields.Many2many(
        comodel_name='stock.picking.package.preparation',
        relation='stock_picking_pack_prepare_rel',
        column1='stock_picking_id',
        column2='stock_picking_package_preparation_id',
        string='DdT',
        copy=False, )

    def _get_invoice_vals(self, cr, uid, key, inv_type, journal_id, move,
                          context=None):
        if not context:
            context = {}
        values = super(StockPicking, self)._get_invoice_vals(
            cr, uid, key, inv_type, journal_id, move, context)
        # ----- Force to use partner invoice from ddt as invoice partner
        if context.get('ddt_partner_id', False):
            values['partner_id'] = context['ddt_partner_id']
        return values

    @api.multi
    def write(self, values):
        pack_to_update = self.env['stock.picking.package.preparation']
        for picking in self:
            pack_to_update |= picking.package_id
        res = super(StockPicking, self).write(values)
        if pack_to_update:
            pack_to_update._update_line_ids()
        return res

    @api.multi
    def unlink(self):
        pack_to_update = self.env['stock.picking.package.preparation']
        for picking in self:
            pack_to_update |= picking.package_id
        res = super(StockPicking, self).unlink()
        if pack_to_update:
            pack_to_update._update_line_ids()
        return res

    @api.model
    def create(self, values):
        picking = super(StockPicking, self).create(values)
        if picking.package_id:
            picking.package_id._update_line_ids()
        return picking
