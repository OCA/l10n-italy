# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
#    Copyright (C) Francesco Apruzzese
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp import fields, models, api


class ddt_from_pickings(models.TransientModel):

    _name = "ddt.from.pickings"

    def _get_move_ids(self):
        return self.env['stock.move'].search(
            [('picking_id', 'in', self.env.context['active_ids']),
             ('ddt_line_id', '=', False),
             ])

    def _get_picking_ids(self):
        return self.env['stock.picking'].browse(self.env.context['active_ids'])

    picking_ids = fields.Many2many('stock.picking', default=_get_picking_ids)
    move_ids = fields.Many2many('stock.move', default=_get_move_ids)

    @api.multi
    def create_ddt(self):
        wizard = self[0]
        picking_ids = self.env.context['active_ids']
        first_picking = self.env['stock.picking'].browse(picking_ids[0])
        ddt = self.env['stock.ddt'].create({
            'partner_id':
            first_picking.partner_id and first_picking.partner_id.id or False,
            'picking_ids': [(6, 0, picking_ids)],
            })
        ddt.create_details(wizard.move_ids)
        # ----- Show new ddt
        ir_model_data = self.env['ir.model.data']
        form_res = ir_model_data.get_object_reference('l10n_it_ddt', 'stock_ddt_form')
        form_id = form_res and form_res[1] or False
        tree_res = ir_model_data.get_object_reference('l10n_it_ddt', 'stock_ddt_tree')
        tree_id = tree_res and tree_res[1] or False
        return {
            'name': 'DdT',
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'stock.ddt',
            'res_id': ddt.id,
            'view_id': False,
            'views': [(form_id, 'form'), (tree_id, 'tree')],
            'type': 'ir.actions.act_window',
        }
