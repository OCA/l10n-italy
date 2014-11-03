# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Davide Corio <info@davidecorio.com>
#    Copyright (C) Davide Corio
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


from openerp import api, models, fields, _
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
        return self.env['ir.sequence'].search(
            [('code', '=', 'stock.ddt')]).id

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

    # ----- Use this function to create line from external resource
    def create_details(self, lines):
        seq = 10
        partner_id = False
        for line in lines:
            if not partner_id:
                partner_id = line.picking_id.partner_id
            # ----- Validate merge only for picking of the same partner
            if line.picking_id.partner_id != partner_id:
                raise Warning(
                    _('Picking related partner must be the same (%s)'
                        % line.picking_id.name))
            ddt_line = self.ddt_lines.create(
                {'sequence': seq,
                 'ddt_id': self.id,
                 'product_id': line.product_id.id,
                 'name': line.name,
                 'product_uom_id': line.product_uom.id,
                 'quantity': line.product_uom_qty,
                 })
            line.write({'ddt_line_id': ddt_line.id})
            seq += 10

    @api.one
    def updateLines(self):
        self.ddt_lines.unlink()
        move_lines = []
        for picking in self.picking_ids:
            move_lines.append(picking.move_lines)
        self.create_details(move_lines)

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


class StockDdTLine(models.Model):

    _name = 'stock.ddt.line'
    _description = 'DdT Line'

    sequence = fields.Integer(string='Sequence')
    name = fields.Char(string='Name')
    ddt_id = fields.Many2one('stock.ddt', string='DdT', ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity')
    product_uom_id = fields.Many2one('product.uom', string='UoM')

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
