# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Abstract (http://www.abstract.it)
#    @author Davide Corio <davide.corio@abstract.it>
#    Copyright (C) 2014 Agile Business Group (http://www.agilebg.com)
#    Copyright (C) 2015 Apulia Software s.r.l. (http://www.apuliasoftware.it)
#    @author Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
##############################################################################


from odoo import fields, models, api


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def _compute_ddt_ids(self):
        for so in self:
            ddt_ids = []
            for picking in so.picking_ids:
                for ddt in picking.ddt_ids:
                    ddt_ids.append(ddt.id)
            so.ddt_ids = ddt_ids

    carriage_condition_id = fields.Many2one(
        'stock.picking.carriage_condition', string='Carriage Condition')
    goods_description_id = fields.Many2one(
        'stock.picking.goods_description',
        string='Description of Goods')
    transportation_reason_id = fields.Many2one(
        'stock.picking.transportation_reason',
        string='Reason for Transportation')
    transportation_method_id = fields.Many2one(
        'stock.picking.transportation_method',
        string='Method of Transportation')
    ddt_carrier_id = fields.Many2one(
        'res.partner', string='Carrier')
    parcels = fields.Integer('Parcels')
    weight = fields.Float(string="Weight")
    volume = fields.Float('Volume')
    ddt_ids = fields.Many2many(
        'stock.picking.package.preparation',
        string='Related DdTs',
        compute='_compute_ddt_ids')
    create_ddt = fields.Boolean('Automatically create the DDT')
    ddt_invoicing_group = fields.Selection(
        [('nothing', 'One DDT - One Invoice'),
         ('billing_partner', 'Billing Partner'),
         ('shipping_partner', 'Shipping Partners'),
         ('code_group', 'Code group')], 'DDT invoicing group',
        default='billing_partner')

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        result = super(SaleOrder, self).onchange_partner_id()
        if self.partner_id:
            self.carriage_condition_id = (
                self.partner_id.carriage_condition_id.id)
            self.goods_description_id = self.partner_id.goods_description_id.id
            self.transportation_reason_id = (
                self.partner_id.transportation_reason_id.id)
            self.transportation_method_id = (
                self.partner_id.transportation_method_id.id)
            self.ddt_invoicing_group = (
                self.partner_id.ddt_invoicing_group)
        return result

    @api.multi
    def _prepare_invoice(self):
        vals = super(SaleOrder, self)._prepare_invoice()
        vals.update({
            'carriage_condition_id': self.carriage_condition_id.id,
            'goods_description_id': self.goods_description_id.id,
            'transportation_reason_id': self.transportation_reason_id.id,
            'transportation_method_id': self.transportation_method_id.id,
            'carrier_id': self.ddt_carrier_id.id,
            'parcels': self.parcels,
            'weight': self.weight,
            'volume': self.volume,
        })
        return vals

    def _preparare_ddt_data(self):
        picking_ids = [p.id for p in self.picking_ids]
        return {
            'partner_id': self.partner_id.id,
            'partner_shipping_id': self.partner_shipping_id.id,
            'carriage_condition_id': self.carriage_condition_id.id,
            'goods_description_id': self.goods_description_id.id,
            'transportation_reason_id':
            self.transportation_reason_id.id,
            'transportation_method_id':
            self.transportation_method_id.id,
            'carrier_id': self.ddt_carrier_id.id,
            'parcels': self.parcels,
            'weight': self.weight,
            'volume': self.volume,
            'picking_ids': [(6, 0, picking_ids)],
        }

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        ddt_model = self.env['stock.picking.package.preparation']
        for order in self:
            if order.create_ddt:
                ddt_data = order._preparare_ddt_data()
                ddt_model.create(ddt_data)
        return res

    @api.multi
    def action_view_ddt(self):
        mod_obj = self.env['ir.model.data']
        act_obj = self.env['ir.actions.act_window']

        result = mod_obj.get_object_reference(
            'stock_picking_package_preparation',
            'action_stock_picking_package_preparation')
        id = result and result[1] or False
        result = act_obj.browse(id).read()[0]

        ddt_ids = []
        for so in self:
            ddt_ids += [ddt.id for ddt in so.ddt_ids]

        if len(ddt_ids) > 1:
            result['domain'] = "[('id','in',[" + ','.join(
                map(str, ddt_ids)) + "])]"
        else:
            res = mod_obj.get_object_reference(
                'stock_picking_package_preparation',
                'stock_picking_package_preparation_form')
            result['views'] = [(res and res[1] or False, 'form')]
            result['res_id'] = ddt_ids and ddt_ids[0] or False
        return result
