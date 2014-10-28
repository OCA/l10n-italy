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


class StockDdTLine(models.Model):
    _name = 'stock.ddt.line'
    _description = 'DdT Line'

    sequence = fields.Integer(string='Sequence')
    name = fields.Char(string='Name')
    ddt_id = fields.Many2one('stock.ddt', string='DdT')
    picking = fields.Many2one('stock.picking', string='Picking')
    product = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity')
    product_uom = fields.Many2one('product.uom', string='UoM')

    _order = 'sequence asc, id'


class StockDdT(models.Model):
    _name = 'stock.ddt'
    _description = 'DdT'

    @api.multi
    def get_sequence(self):
        return self.env['ir.sequence'].search(
            [('code', '=', 'stock.ddt')]).id

    name = fields.Char(string='Number')
    delivery_date = fields.Datetime(string='Date', required=True)
    sequence = fields.Many2one(
        'ir.sequence', string='Sequence',
        default=get_sequence, required=True)
    pickings = fields.Many2many('stock.picking', string='Pickings')
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
    state = fields.Selection(
        [('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled')],
        string='State',
        default='draft'
        )

    @api.model
    def create(self, values):
        sequence_model = self.env['ir.sequence']
        sequence = sequence_model.browse(values['sequence'])
        values['name'] = sequence_model.get(sequence.code)
        return super(StockDdT, self).create(values)

    @api.multi
    def write(self, values):
        result = super(StockDdT, self).write(values)
        if values.get('pickings'):
            picking_model = self.env['stock.picking']
            pickings = picking_model.browse(values['pickings'][0][2])
            pickings.write({'ddt_id': self.id})
        return result

    @api.one
    def updateLines(self):
        self.ddt_lines.unlink()
        seq = 0
        for picking in self.pickings:
            if picking.partner_id != self.partner_id:
                raise Warning(
                    _('Picking related partner must be the same (%s)'
                        % picking.name))
            for move in picking.move_lines:
                if not seq:
                    seq = 10
                else:
                    seq += 10
                self.ddt_lines.create(
                    {
                        'sequence': seq,
                        'ddt_id': self.id,
                        'picking': move.picking_id.id,
                        'product': move.product_id.id,
                        'name': move.name,
                        'product_uom': move.product_uom.id,
                        'quantity': move.product_uom_qty,
                        })

    @api.multi
    def action_confirm(self):
        self.write({'state': 'confirmed'})

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancelled'})


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
                })
        return res
