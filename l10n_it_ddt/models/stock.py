# -*- coding: utf-8 -*-
# Copyright 2015 Apulia Software s.r.l. (http://www.apuliasoftware.it)
# @author Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    ddt_ids = fields.Many2many(
        comodel_name='stock.picking.package.preparation',
        relation='stock_picking_pack_prepare_rel',
        column1='stock_picking_id',
        column2='stock_picking_package_preparation_id',
        string='DdT',
        copy=False, )

    @api.multi
    @api.constrains('state')
    def _ddt_constrain_state(self):
        """Prevent pickings that are included in a DDT to be set as done
        unless it is being processed by DDT"""
        if self.env.context.get('ddt_processing', False):
            return
        for picking in self:
            if picking.state == 'done' and picking.ddt_ids:
                raise ValidationError(
                    _('Cannot set to "Done" picking %s '
                      'because it is included in DDT %s.\n'
                      'Process the DDT or unlink the picking from the DDT.')
                    % (picking.display_name,
                       picking.ddt_ids[0].display_name))

    @api.multi
    def write(self, values):
        pack_to_update = None
        if 'move_lines' in values:
            pack_to_update = self.env['stock.picking.package.preparation']
            for picking in self:
                pack_to_update |= picking.ddt_ids
        res = super(StockPicking, self).write(values)
        if pack_to_update:
            pack_to_update._update_line_ids()
        return res

    @api.multi
    def unlink(self):
        pack_to_update = self.env['stock.picking.package.preparation']
        for picking in self:
            pack_to_update |= picking.ddt_ids
        res = super(StockPicking, self).unlink()
        if pack_to_update:
            pack_to_update._update_line_ids()
        return res

    @api.model
    def create(self, values):
        picking = super(StockPicking, self).create(values)
        if picking.ddt_ids:
            picking.ddt_ids._update_line_ids()
        return picking

    def get_ddt_shipping_partner(self):
        # this is mainly used in dropshipping configuration,
        # where self.partner_id is your supplier, but 'move_lines.partner_id'
        # is your customer
        if not self.picking_type_code == 'internal':
            move_partners = self.mapped('move_lines.partner_id')
            if len(move_partners) == 1:
                return move_partners[0]
            else:
                return self.partner_id
        else:
            return self.location_dest_id.partner_id
