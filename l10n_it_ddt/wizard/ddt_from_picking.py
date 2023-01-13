# Copyright 2014 Abstract (http://www.abstract.it)
# Copyright Davide Corio <davide.corio@abstract.it>
# Copyright 2014-2018 Agile Business Group (http://www.agilebg.com)
# Copyright 2015 Apulia Software s.r.l. (http://www.apuliasoftware.it)
# Copyright Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, _
from odoo.exceptions import Warning as UserError


class DdTFromPickings(models.TransientModel):
    _name = "ddt.from.pickings"
    _description = 'TD from pickings'

    def _get_picking_ids(self):
        return self.env['stock.picking'].browse(self.env.context['active_ids'])

    picking_ids = fields.Many2many('stock.picking', default=_get_picking_ids)

    def _set_default_note(self, values):
        """Set note only if all involved TD types have the same default note."""
        td_types_notes = self.picking_ids.mapped('ddt_type.default_note')
        # Exclude falsy notes
        td_types_notes = list(filter(None, td_types_notes))
        if len(td_types_notes) == 1:
            td_types_note = td_types_notes.pop()
            values['note'] = td_types_note

    @api.multi
    def create_ddt(self):
        values = {
            'partner_id': False,
            'parcels': 0,
            'carriage_condition_id': False,
            'goods_description_id': False,
            'transportation_reason_id': False,
            'transportation_method_id': False,
            'carrier_id': False,
        }
        type_list = []
        partner = False
        for picking in self.picking_ids:
            # check if picking is already linked to a DDT
            self.env['stock.picking.package.preparation'].check_linked_picking(
                picking)
            current_ddt_shipping_partner = picking.get_ddt_shipping_partner()
            if partner and partner != current_ddt_shipping_partner:
                raise UserError(
                    _("Selected Pickings have different Partner"))
            partner = current_ddt_shipping_partner
            sale_order = picking.sale_id
            if sale_order:
                values['ddt_show_price'] = sale_order.ddt_show_price
                values['partner_id'] = sale_order.partner_id.id
            else:
                values['ddt_show_price'] = partner.ddt_show_price
                values['partner_id'] = partner.commercial_partner_id.id
            if not picking.picking_type_code == 'internal':
                values['partner_shipping_id'] = partner.id
            else:
                values['partner_shipping_id'] = (
                    picking.location_dest_id.partner_id.id)
            # get ddt type from the first picking
            if picking.ddt_type:
                type_list.append(picking.ddt_type.id)
        # check if selected picking have different destinations
        if len(self.picking_ids.mapped('location_dest_id')) > 1:
            raise UserError(_("Selected pickings have different destinations"))
        if len(type_list) > 0:
            values.update(
                {'ddt_type_id': type_list[0]})
        parcels = 0
        # for each of the following fields (carriage condition id,
        # goods description id, transportation id, transportation method)
        # get values from sale id, else from partner, else from ddt type
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
            elif picking.partner_id and \
                    picking.partner_id.carriage_condition_id:
                carriage_condition_id = (
                    picking.partner_id.carriage_condition_id)
                values['carriage_condition_id'] = (
                    carriage_condition_id.id)
            elif picking.ddt_type and \
                    picking.ddt_type.default_carriage_condition_id:
                carriage_condition_id = (
                    picking.ddt_type.default_carriage_condition_id)
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
            elif picking.partner_id and \
                    picking.partner_id.goods_description_id:
                goods_description_id = (
                    picking.partner_id.goods_description_id)
                values['goods_description_id'] = (
                    goods_description_id.id)
            elif picking.ddt_type and \
                    picking.ddt_type.default_goods_description_id:
                goods_description_id = (
                    picking.ddt_type.default_goods_description_id)
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
            elif picking.partner_id and \
                    picking.partner_id.transportation_reason_id:
                transportation_reason_id = (
                    picking.partner_id.transportation_reason_id)
                values['transportation_reason_id'] = (
                    transportation_reason_id.id)
            elif picking.ddt_type and \
                    picking.ddt_type.default_transportation_reason_id:
                transportation_reason_id = (
                    picking.ddt_type.default_transportation_reason_id)
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
            elif picking.partner_id \
                    and picking.partner_id.transportation_method_id:
                transportation_method_id = (
                    picking.partner_id.transportation_method_id)
                values['transportation_method_id'] = (
                    transportation_method_id.id)
            elif picking.ddt_type and \
                    picking.ddt_type.default_transportation_method_id:
                transportation_method_id = (
                    picking.ddt_type.default_transportation_method_id)
                values['transportation_method_id'] = (
                    transportation_method_id.id)
        self._set_default_note(values)
        carrier_id = False
        for picking in self.picking_ids:
            if picking.sale_id and picking.sale_id.ddt_carrier_id:
                if carrier_id and (
                    carrier_id != (
                        picking.sale_id.ddt_carrier_id)):
                    raise UserError(
                        _("Selected Pickings have "
                          "different carrier"))
                carrier_id = picking.sale_id.ddt_carrier_id
                values['carrier_id'] = (
                    carrier_id.id)

        if transportation_reason_id:
            values['to_be_invoiced'] = transportation_reason_id.to_be_invoiced

        if len(self.picking_ids) == 1 and self.picking_ids[0].sale_id:
            # otherwise weights and volume should be different
            values['weight_manual'] = self.picking_ids[0].sale_id.weight
            values['gross_weight'] = self.picking_ids[0].sale_id.gross_weight
            values['volume'] = self.picking_ids[0].sale_id.volume

        picking_ids = self.picking_ids.ids
        values.update({'picking_ids': [(6, 0, picking_ids)]})
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
            'name': _('TD'),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'stock.picking.package.preparation',
            'res_id': ddt.id,
            'view_id': False,
            'views': [(form_id, 'form'), (tree_id, 'tree')],
            'type': 'ir.actions.act_window',
        }
