# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Apulia Software s.r.l. (http://www.apuliasoftware.it)
#    @author Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
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


from openerp import models, fields, api, exceptions, _


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


class StockDdtType(models.Model):

    _name = 'stock.ddt.type'
    _description = 'Stock DdT Type'
    _inherit = ['mail.thread']

    name = fields.Char(required=True)
    sequence_id = fields.Many2one('ir.sequence', required=True)
    note = fields.Text(string='Note')


class StockPickingPackagePreparation(models.Model):

    _inherit = 'stock.picking.package.preparation'
    _rec_name = 'display_name'

    ddt_type_id = fields.Many2one('stock.ddt.type',
                                  string='DdT Type')
    ddt_number = fields.Char(string='DdT Number')
    partner_invoice_id = fields.Many2one('res.partner')
    partner_shipping_id = fields.Many2one('res.partner')
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
    display_name = fields.Char(string='Name', compute='_compute_display_name')
    volume = fields.Float('Volume')

    @api.onchange('partner_id', 'ddt_type_id')
    def on_change_partner(self):
        if self.ddt_type_id:
            self.partner_invoice_id = self.partner_id
            self.partner_shipping_id = self.partner_id

    @api.multi
    def action_put_in_pack(self):
        for package in self:
            # ----- Assign ddt number if ddt type is set
            if package.ddt_type_id and not package.ddt_number:
                package.ddt_number = package.ddt_type_id.sequence_id.get(
                    package.ddt_type_id.sequence_id.code)
        return super(StockPickingPackagePreparation, self).action_put_in_pack()

    @api.one
    @api.depends('name', 'ddt_number', 'partner_id', 'date')
    def _compute_display_name(self):
        name = ''
        if self.name:
            name = self.name
        if self.ddt_number and self.name:
            name = '[{package}] {ddt}'.format(package=self.name,
                                              ddt=self.ddt_number)
        if self.ddt_number and not self.name:
            name = self.ddt_number
        if not name:
            name = '{partner} of {date}'.format(partner=self.partner_id.name,
                                                date=self.date)
        self.display_name = name


class StockPickingPackagePreparationLine(models.Model):

    _inherit = 'stock.picking.package.preparation.line'

    invoiceable = fields.Selection(
        [('none', 'None'), ('invoiceable', 'Invoiceable')],
        default='invoiceable')

    @api.multi
    def get_move_data(self):
        move_data = super(StockPickingPackagePreparationLine,
                          self).get_move_data()
        if self.invoiceable == 'invoiceable':
            move_data.update({
                'invoice_state': '2binvoiced',
                })
        return move_data
