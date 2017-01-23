# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2015 Nicola Malcontenti - Agile Business Group
#    Copyright (C) 2015 Apulia Software s.r.l. (http://www.apuliasoftware.it)
#    @author Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
##############################################################################


from odoo import fields, models, api, _
from odoo.exceptions import Warning as UserError


class AddPickingToDdt(models.TransientModel):

    _name = "add.pickings.to.ddt"

    ddt_id = fields.Many2one('stock.picking.package.preparation')

    @api.multi
    def add_to_ddt(self):
        pickings = self.env['stock.picking'].browse(
            self.env.context['active_ids'])
        for picking in pickings:
            # check if picking is already linked to a DDT
            self.env['stock.picking.package.preparation'].check_linked_picking(
                picking)
            current_ddt_shipping_partner = picking.get_ddt_shipping_partner()
            if picking.ddt_ids and \
                    self.ddt_id.id in [d.id for d in picking.ddt_ids]:
                raise UserError(
                    _("Picking %s already in ddt") % picking.name)
            elif (
                current_ddt_shipping_partner != self.ddt_id.partner_shipping_id
            ):
                raise UserError(
                    _("Selected Picking %s have"
                      " different Partner") % picking.name)
            if picking.sale_id:
                if picking.sale_id.carriage_condition_id != (
                        self.ddt_id.carriage_condition_id):
                    raise UserError(
                        _("Selected Picking %s have"
                          " different carriage condition") % picking.name)
                elif picking.sale_id.goods_description_id != (
                        self.ddt_id.goods_description_id):
                    raise UserError(
                        _("Selected Picking %s have "
                          "different goods description") % picking.name)
                elif picking.sale_id.transportation_reason_id != (
                        self.ddt_id.transportation_reason_id):
                    raise UserError(
                        _("Selected Picking %s have"
                          " different transportation reason") % picking.name)
                elif picking.sale_id.transportation_method_id != (
                        self.ddt_id.transportation_method_id):
                    raise UserError(
                        _("Selected Picking %s have"
                          " different transportation reason") % picking.name)
            self.ddt_id.picking_ids = [(4, picking.id)]
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
            'res_id': self.ddt_id.id,
            'view_id': False,
            'views': [(form_id, 'form'), (tree_id, 'tree')],
            'type': 'ir.actions.act_window',
        }
