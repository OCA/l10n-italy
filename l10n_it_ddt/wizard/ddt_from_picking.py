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


from odoo import fields, models, api


class DdTFromPickings(models.TransientModel):

    _name = "ddt.from.pickings"

    def _get_picking_ids(self):
        return self.env['stock.picking'].browse(self.env.context['active_ids'])

    picking_ids = fields.Many2many('stock.picking', default=_get_picking_ids)

    @api.multi
    def create_ddt(self):
        ddt_ids = []
        for picking in self.picking_ids:
            values = {}
            # check if picking is already linked to a DDT
            self.env['stock.picking.package.preparation'].check_linked_picking(
                picking)
            partner = picking.get_ddt_shipping_partner()
            sale_order = picking.sale_id
            if sale_order:
                values['partner_id'] = sale_order.partner_id.id
            else:
                values['partner_id'] = partner.commercial_partner_id.id
            if not picking.picking_type_code == 'internal':
                values['partner_shipping_id'] = partner.id
            else:
                values['partner_shipping_id'] = (
                    picking.location_dest_id.partner_id.id)
            values['parcels'] = (
                picking.sale_id and picking.sale_id.parcels or 0)
            values['carriage_condition_id'] = (
                picking.sale_id and
                picking.sale_id.carriage_condition_id and
                picking.sale_id.carriage_condition_id.id)
            values['goods_description_id'] = (
                picking.sale_id and
                picking.sale_id.goods_description_id and
                picking.sale_id.goods_description_id.id)
            values['transportation_reason_id'] = (
                picking.sale_id and
                picking.sale_id.transportation_reason_id and
                picking.sale_id.transportation_reason_id.id)
            values['transportation_method_id'] = (
                picking.sale_id and
                picking.sale_id.transportation_method_id and
                picking.sale_id.transportation_method_id.id)
            values.update({
                'picking_ids': [(6, 0, self.picking_ids.ids)]})
            ddt = self.env['stock.picking.package.preparation'].create(values)
            ddt_ids.append(ddt.id)
        # ----- Show new ddts
        ir_model_data = self.env['ir.model.data']
        result = ir_model_data.get_object_reference(
            'stock_picking_package_preparation',
            'action_stock_picking_package_preparation')
        id = result and result[1] or False
        result = self.env['ir.actions.act_window'].browse(id).read()[0]
        if len(ddt_ids) > 1:
            result['domain'] = "[('id','in',[" + ','.join(
                map(str, ddt_ids)) + "])]"
        else:
            res = ir_model_data.get_object_reference(
                'stock_picking_package_preparation',
                'stock_picking_package_preparation_form')
            result['views'] = [(res and res[1] or False, 'form')]
            result['res_id'] = ddt_ids and ddt_ids[0] or False
        return result
