# Copyright 2014 Abstract (http://www.abstract.it)
# Copyright Davide Corio <davide.corio@abstract.it>
# Copyright 2014-2018 Agile Business Group (http://www.agilebg.com)
# Copyright 2015 Apulia Software s.r.l. (http://www.apuliasoftware.it)
# Copyright Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    ddt_ids = fields.Many2many(
        comodel_name='stock.picking.package.preparation',
        relation='stock_picking_pack_prepare_rel',
        column1='stock_picking_id',
        column2='stock_picking_package_preparation_id',
        string='TD',
        copy=False, )

    ddt_supplier_number = fields.Char(string='Supplier TD Number', copy=False)
    ddt_supplier_date = fields.Date(string='Supplier TD Date', copy=False)
    ddt_type = fields.Many2one(
        'stock.ddt.type',
        related='picking_type_id.default_location_src_id.type_ddt_id')

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

    @api.multi
    def open_form_current(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': self._name,
            'res_id': self.id,
            'target': 'current'
        }
