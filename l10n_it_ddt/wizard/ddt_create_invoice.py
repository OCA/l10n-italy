# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Abstract (http://www.abstract.it)
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


from openerp import models, api, fields
from openerp.tools.translate import _
from openerp.exceptions import Warning


class DdTCreateInvoice(models.TransientModel):

    _name = "ddt.create.invoice"
    _rec_name = "journal_id"

    journal_id = fields.Many2one('account.journal', 'Journal', required=True)
    date = fields.Date('Date')

    def check_ddt_data(self, ddts):
        carriage_condition_id = False
        goods_description_id = False
        transportation_reason_id = False
        transportation_method_id = False
        parcels = False
        for ddt in ddts:
            if (
                carriage_condition_id and
                ddt.carriage_condition_id.id != carriage_condition_id
            ):
                raise Warning(
                    _("Selected DDTs have different Carriage Conditions"))
            if (
                goods_description_id and
                ddt.goods_description_id.id != goods_description_id
            ):
                raise Warning(
                    _("Selected DDTs have different Descriptions of Goods"))
            if (
                transportation_reason_id and
                ddt.transportation_reason_id.id != transportation_reason_id
            ):
                raise Warning(
                    _("Selected DDTs have different "
                      "Reasons for Transportation"))
            if (
                transportation_method_id and
                ddt.transportation_method_id.id != transportation_method_id
            ):
                raise Warning(
                    _("Selected DDTs have different "
                      "Methods of Transportation"))
            if (
                parcels and
                ddt.parcels != parcels
            ):
                raise Warning(
                    _("Selected DDTs have different parcels"))

    @api.multi
    def create_invoice(self):
        ddt_model = self.env['stock.ddt']
        picking_pool = self.pool['stock.picking']

        ddts = ddt_model.browse(self.env.context['active_ids'])
        partners = set([ddt.partner_id for ddt in ddts])
        if len(partners) > 1:
            raise Warning(_("Selected DDTs belong to different partners"))
        pickings = []
        self.check_ddt_data(ddts)
        for ddt in ddts:
            for picking in ddt.picking_ids:
                pickings.append(picking.id)
                for move in picking.move_lines:
                    if move.invoice_state != "2binvoiced":
                        raise Warning(
                            _("Move %s is not invoiceable") % move.name)
        invoices = picking_pool.action_invoice_create(
            self.env.cr,
            self.env.uid,
            pickings,
            self.journal_id.id, group=True, context=None)
        invoice_obj = self.env['account.invoice'].browse(invoices)
        invoice_obj.write({
            'carriage_condition_id': ddts[0].carriage_condition_id.id,
            'goods_description_id': ddts[0].goods_description_id.id,
            'transportation_reason_id': ddts[0].transportation_reason_id.id,
            'transportation_method_id': ddts[0].transportation_method_id.id,
            'parcels': ddts[0].parcels,
            })
        ir_model_data = self.env['ir.model.data']
        form_res = ir_model_data.get_object_reference('account',
                                                      'invoice_form')
        form_id = form_res and form_res[1] or False
        tree_res = ir_model_data.get_object_reference('account',
                                                      'invoice_tree')
        tree_id = tree_res and tree_res[1] or False
        return {
            'name': 'Invoice',
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'account.invoice',
            'res_id': invoices[0],
            'view_id': False,
            'views': [(form_id, 'form'), (tree_id, 'tree')],
            'type': 'ir.actions.act_window',
        }
