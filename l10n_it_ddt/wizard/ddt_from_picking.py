# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
#    Copyright (C) Francesco Apruzzese
#    Copyright (C) 2014-2015 Agile Business Group (http://www.agilebg.com)
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
##############################################################################


from openerp import fields, models, api, _
from openerp.exceptions import Warning as UserError


class DdTFromPickings(models.TransientModel):

    _name = "ddt.from.pickings"

    def _get_picking_ids(self):
        return self.env['stock.picking'].browse(self.env.context['active_ids'])

    picking_ids = fields.Many2many('stock.picking', default=_get_picking_ids)

    @api.multi
    def create_ddt(self):
        values = {
            'partner_id': False,
            'parcels': 0,
            'carriage_condition_id': False,
            'goods_description_id': False,
            'transportation_reason_id': False,
            'transportation_method_id': False
            }
        partner = False
        for picking in self.picking_ids:
            current_ddt_shipping_partner = picking.get_ddt_shipping_partner()
            if partner and partner != current_ddt_shipping_partner:
                raise UserError(
                    _("Selected Pickings have different Partner"))
            partner = current_ddt_shipping_partner
            sale_order = picking.sale_id
            if sale_order:
                values['partner_id'] = sale_order.partner_id.id
            else:
                values['partner_id'] = partner.commercial_partner_id.id
            values['partner_shipping_id'] = partner.id
        parcels = 0
        for picking in self.picking_ids:
            if picking.sale_id and picking.sale_id.parcels:
                if parcels and parcels != picking.sale_id.parcels:
                    raise UserError(
                        _("Selected Pickings have different parcels"))
                parcels = picking.sale_id.parcels
                values['parcels'] = parcels
        carriage_condition_id = False
        for picking in self.picking_ids:
            if picking.sale_id and picking.sale_id.carriage_condition_id:
                if carriage_condition_id and (
                        carriage_condition_id != (
                            picking.sale_id.carriage_condition_id)):
                    raise UserError(
                        _("Selected Pickings have"
                          " different carriage condition"))
                carriage_condition_id = (
                    picking.sale_id.carriage_condition_id)
                values['carriage_condition_id'] = (
                    carriage_condition_id.id)
        goods_description_id = False
        for picking in self.picking_ids:
            if picking.sale_id and picking.sale_id.goods_description_id:
                if goods_description_id and (
                    goods_description_id != (
                        picking.sale_id.goods_description_id)):
                    raise UserError(
                        _("Selected Pickings have "
                          "different goods description"))
                goods_description_id = picking.sale_id.goods_description_id
                values['goods_description_id'] = (
                    goods_description_id.id)
        transportation_reason_id = False
        for picking in self.picking_ids:
            if picking.sale_id and (
                    picking.sale_id.transportation_reason_id):
                if transportation_reason_id and (
                        transportation_reason_id != (
                            picking.sale_id.transportation_reason_id)):
                    raise UserError(
                        _("Selected Pickings have"
                            " different transportation reason"))
                transportation_reason_id = (
                    picking.sale_id.transportation_reason_id)
                values['transportation_reason_id'] = (
                    transportation_reason_id.id)
        transportation_method_id = False
        for picking in self.picking_ids:
            if picking.sale_id and (
                    picking.sale_id.transportation_method_id):
                if transportation_method_id and (
                    transportation_method_id != (
                        picking.sale_id.transportation_method_id)):
                    raise UserError(
                        _("Selected Pickings have"
                          " different transportation method"))
                transportation_method_id = (
                    picking.sale_id.transportation_method_id)
                values['transportation_method_id'] = (
                    transportation_method_id.id)
        picking_ids = [p.id for p in self.picking_ids]
        values.update({
            'picking_ids': [(6, 0, picking_ids)]
            })
        ddt = self.env['stock.picking.package.preparation'].create(values)
        # ----- Show new ddt
        ir_model_data = self.env['ir.model.data']
        form_res = ir_model_data.get_object_reference(
            'stock_picking_package_preparation',
            'stock_picking_package_preparation_form')
        form_id = form_res and form_res[1] or False
        tree_res = ir_model_data.get_object_reference(
            'stock_picking_package_preparation',
            'stock_picking_package_preparation_tree')
        tree_id = tree_res and tree_res[1] or False
        return {
            'name': 'DdT',
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'stock.picking.package.preparation',
            'res_id': ddt.id,
            'view_id': False,
            'views': [(form_id, 'form'), (tree_id, 'tree')],
            'type': 'ir.actions.act_window',
        }
