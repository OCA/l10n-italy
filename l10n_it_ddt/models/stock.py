# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Abstract (http://www.abstract.it)
#    @author Davide Corio <davide.corio@abstract.it>
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

    name = fields.Char(string='Number')
    date = fields.Datetime(required=True, default=fields.Datetime.now())
    delivery_date = fields.Datetime()
    sequence = fields.Many2one(
        'ir.sequence', string='Sequence',
        default=get_sequence, required=True)
    picking_ids = fields.Many2many('stock.picking', string='Pickings')
    ddt_lines = fields.One2many(
        'stock.ddt.line', 'ddt_id', string='DdT Line')
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

    @api.multi
    def write(self, values):
        result = super(StockDdT, self).write(values)
        if values.get('picking_ids'):
            picking_model = self.env['stock.picking']
            pickings = picking_model.browse(values['picking_ids'][0][2])
            pickings.write({'ddt_id': self.id})
        return result

    @api.model
    def create(self, values):
        result = super(StockDdT, self).create(values)
        result.updateLines()
        return result

    def get_ddt_line_values(self, seq, move_line):
        """ get DdT line values given `seq` number and a `move_line`
        """
        values = {
            'sequence': seq,
            'ddt_id': self.id,
            'product_id': move_line.product_id.id,
            'name': move_line.name,
            'product_uom_id': move_line.product_uom.id,
            'quantity': move_line.product_uom_qty,
            'move_line_id': move_line.id
        }
        return values

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
            move_line.write({'ddt_line_id': ddt_line.id})
            seq += 10

    @api.one
    def updateLines(self):
        self.ddt_lines.unlink()
        move_lines = []
        for picking in self.picking_ids:
            move_lines.extend(picking.move_lines)
        self.create_lines(move_lines)

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
    def name_get(self):
        result = []
        for ddt in self:
            result.append((ddt.id, "%s" % (ddt.name or 'N/A')))
        return result


class StockDdTLine(models.Model):

    _name = 'stock.ddt.line'
    _description = 'DdT Line'

    sequence = fields.Integer(string='Sequence')
    name = fields.Char(string='Name')
    ddt_id = fields.Many2one('stock.ddt', string='DdT', ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity')
    product_uom_id = fields.Many2one('product.uom', string='UoM')
    move_line_id = fields.Many2one('stock.move', ondelete="set null")

    _order = 'sequence asc, id'


class StockPicking(models.Model):

    _inherit = "stock.picking"

    carriage_condition_id = fields.Many2one(
        'stock.picking.carriage_condition', string='Carriage Condition')
    goods_description_id = fields.Many2one(
        'stock.picking.goods_description', string='Description of Goods')
    transportation_reason_id = fields.Many2one(
        'stock.picking.transportation_reason',
        string='Reason for Transportation')
    transportation_method_id = fields.Many2one(
        'stock.picking.transportation_method',
        string='Method of Transportation')
    parcels = fields.Integer()
    ddt_id = fields.Many2one('stock.ddt', string='DdT', readonly=True)
    ddt_type = fields.Selection(
        string="DdT Type", related='picking_type_id.code')

    def action_invoice_create(
            self, cr, uid, ids, journal_id, group=False, type='out_invoice',
            context=None):
        if not context:
            context = {}
        invoice_obj = self.pool['account.invoice']
        res = super(StockPicking, self).action_invoice_create(
            cr, uid, ids, journal_id, group, type, context)
        for picking in self.browse(cr, uid, ids, context=context):
            invoice_obj.write(cr, uid, res, {
                'carriage_condition_id':
                picking.carriage_condition_id and
                picking.carriage_condition_id.id,
                'goods_description_id':
                picking.goods_description_id and
                picking.goods_description_id.id,
                'transportation_reason_id':
                picking.transportation_reason_id and
                picking.transportation_reason_id.id,
                'transportation_method_id':
                picking.transportation_method_id and
                picking.transportation_method_id.id,
                'parcels': picking.parcels,
            })
        return res


class StockMove(models.Model):

    _inherit = "stock.move"

    ddt_line_id = fields.Many2one('stock.ddt.line', ondelete="set null")

    @api.cr_uid_ids_context
    def _picking_assign(
        self, cr, uid, move_ids, procurement_group, location_from, location_to,
            context=None):

        res = super(StockMove, self)._picking_assign(
            cr, uid, move_ids, procurement_group, location_from, location_to,
            context=context)

        group_model = self.pool['procurement.group']
        group = group_model.browse(cr, uid, procurement_group)
        ddt = group.ddt_id

        picking_ids = []

        for move in self.browse(cr, uid, move_ids):
            if move.picking_id.id not in picking_ids:
                picking_ids.append(move.picking_id.id)

        ddt.write({'picking_ids': [(6, 0, picking_ids)]})

        return res
