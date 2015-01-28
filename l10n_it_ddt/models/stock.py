# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Abstract (http://www.abstract.it)
#    @author Davide Corio <davide.corio@abstract.it>
#    Copyright (C) 2014 Agile Business Group (http://www.agilebg.com)
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

from openerp import fields
from openerp import models
from openerp import api
from openerp import _
from openerp.exceptions import Warning


class StockPickingCarriageCondition(models.Model):

    _name = "stock.picking.carriage_condition"
    _description = "Carriage Condition"

    name = fields.Char(string='Carriage Condition', required=True)
    note = fields.Text(string='Note')


class StockPickingGoodsDescription(models.Model):

    _name = 'stock.picking.goods_description'
    _description = "Description of Goods"

    name = fields.Char(string='Description of Goods', required=True)
    note = fields.Text(string='Note')


class StockPickingTransportationReason(models.Model):

    _name = 'stock.picking.transportation_reason'
    _description = 'Reason for Transportation'

    name = fields.Char(string='Reason For Transportation', required=True)
    note = fields.Text(string='Note')


class StockPickingTransportationMethod(models.Model):

    _name = 'stock.picking.transportation_method'
    _description = 'Method of Transportation'

    name = fields.Char(string='Method of Transportation', required=True)
    note = fields.Text(string='Note')


class StockDdT(models.Model):

    _name = 'stock.ddt'
    _description = 'DdT'

    @api.multi
    def get_sequence(self):
        # XXX: allow config of default seq per company
        return self.env['ir.sequence'].search(
            [('code', '=', 'stock.ddt')])[0].id

    def _compute_picking_ids(self):
        picking_ids = []
        for ddt in self:
            for line in ddt.ddt_lines:
                if line.move_line_id.picking_id.id not in picking_ids:
                    picking_ids.append(line.move_line_id.picking_id.id)
            ddt.picking_ids = picking_ids

    name = fields.Char(string='Number')
    date = fields.Datetime(required=True, default=fields.Datetime.now())
    delivery_date = fields.Datetime()
    sequence = fields.Many2one(
        'ir.sequence', string='Sequence',
        default=get_sequence, required=True)
    picking_ids = fields.Many2many(
        'stock.picking', string='Pickings', compute="_compute_picking_ids",
        readonly=True)
    ddt_lines = fields.One2many(
        'stock.ddt.line', 'ddt_id', string='DdT Line', readonly=True)
    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True)
    delivery_address_id = fields.Many2one(
        'res.partner', string='Delivery Address', required=False)
    carriage_condition_id = fields.Many2one(
        'stock.picking.carriage_condition', 'Carriage Condition')
    goods_description_id = fields.Many2one(
        'stock.picking.goods_description', 'Description of Goods')
    transportation_reason_id = fields.Many2one(
        'stock.picking.transportation_reason',
        'Reason for Transportation')
    transportation_method_id = fields.Many2one(
        'stock.picking.transportation_method',
        'Method of Transportation')
    carrier_id = fields.Many2one(
        'res.partner', string='Carrier')
    parcels = fields.Integer()
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirmed', 'Confirmed'),
         ('cancelled', 'Cancelled')],
        string='State',
        default='draft'
    )

    def get_ddt_line_values(self, seq, move_line):
        """ get DdT line values given `seq` number and a `move_line`
        """
        values = {
            'sequence': seq,
            'ddt_id': self.id,
            'move_line_id': move_line.id
        }
        return values

    @api.one
    def create_lines(self, move_lines):
        """ create DdT lines
        """
        seq = 10
        partner_id = False
        for move_line in move_lines:
            if not partner_id:
                partner_id = move_line.picking_id.partner_id
            # ----- Validate merge only for picking of the same partner
            if move_line.picking_id.partner_id != partner_id:
                raise Warning(
                    _('Picking related partner must be the same (%s)'
                        % move_line.picking_id.name))
            ddt_line = self.ddt_lines.create(
                self.get_ddt_line_values(seq, move_line)
            )
            seq += 10

    @api.multi
    def set_number(self):
        for ddt in self:
            if not ddt.name:
                ddt.write({
                    'name': ddt.sequence.get(ddt.sequence.code),
                })

    @api.multi
    def action_confirm(self):
        self.write({'state': 'confirmed'})

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancelled'})

    @api.multi
    def action_reopen(self):
        self.write({'state': 'draft'})
        self.delete_workflow()
        self.create_workflow()
        return True

    @api.multi
    def name_get(self):
        result = []
        for ddt in self:
            result.append((ddt.id, "%s" % (ddt.name or 'N/A')))
        return result


class StockDdTLine(models.Model):

    _name = 'stock.ddt.line'
    _description = 'DdT Line'

    sequence = fields.Integer(string='Sequence')
    name = fields.Char(related="move_line_id.name", readonly=True)
    ddt_id = fields.Many2one('stock.ddt', string='DdT', ondelete='cascade')
    product_id = fields.Many2one(
        'product.product', related="move_line_id.product_id", readonly=True)
    quantity = fields.Float(
        related="move_line_id.product_uom_qty", readonly=True)
    product_uom_id = fields.Many2one(
        'product.uom', related="move_line_id.product_uom", readonly=True)
    move_line_id = fields.Many2one('stock.move', required=True)

    _order = 'sequence asc, id'


class StockPicking(models.Model):

    _inherit = "stock.picking"

    def _compute_ddt_ids(self):
        ddt_ids = []
        ddt_line_model = self.env['stock.ddt.line']
        for picking in self:
            for line in picking.move_lines:
                ddt_lines = ddt_line_model.search(
                    [('move_line_id', '=', line.id)])
                for ddt_line in ddt_lines:
                    if ddt_line.ddt_id.id not in ddt_ids:
                        ddt_ids.append(ddt_line.ddt_id.id)
            picking.ddt_ids = ddt_ids

    ddt_ids = fields.Many2many(
        "stock.ddt", string="DDT list", readonly=True,
        compute="_compute_ddt_ids")

class StockMove(models.Model):
    _inherit = "stock.move"
    ddt_line_ids = fields.One2many("stock.ddt.line", "move_line_id")
