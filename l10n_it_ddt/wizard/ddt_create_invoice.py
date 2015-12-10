# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Abstract (http://www.abstract.it)
#    Copyright (C) 2014 Agile Business Group (http://www.agilebg.com)
#    Copyright (C) 2015 Apulia Software s.r.l. (http://www.apuliasoftware.it)
#    @author Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
##############################################################################


from openerp import models, api, fields
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError


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
                raise UserError(
                    _("Selected DDTs have different Carriage Conditions"))
            if (
                goods_description_id and
                ddt.goods_description_id.id != goods_description_id
            ):
                raise UserError(
                    _("Selected DDTs have different Descriptions of Goods"))
            if (
                transportation_reason_id and
                ddt.transportation_reason_id.id != transportation_reason_id
            ):
                raise UserError(
                    _("Selected DDTs have different "
                      "Reasons for Transportation"))
            if (
                transportation_method_id and
                ddt.transportation_method_id.id != transportation_method_id
            ):
                raise UserError(
                    _("Selected DDTs have different "
                      "Methods of Transportation"))
            if (
                parcels and
                ddt.parcels != parcels
            ):
                raise UserError(
                    _("Selected DDTs have different parcels"))

    @api.multi
    def create_invoice(self):
        ddt_model = self.env['stock.picking.package.preparation']
        picking_pool = self.pool['stock.picking']

        ddts = ddt_model.browse(self.env.context['active_ids'])
        partners = set([ddt.partner_invoice_id for ddt in ddts])
        if len(partners) > 1:
            raise UserError(_("Selected DDTs belong to different partners"))
        pickings = []
        self.check_ddt_data(ddts)
        for ddt in ddts:
            for picking in ddt.picking_ids:
                pickings.append(picking.id)
                for move in picking.move_lines:
                    if move.invoice_state != "2binvoiced":
                        raise UserError(
                            _("Move %s is not invoiceable") % move.name)
        # ----- Force to use partner invoice from ddt as invoice partner
        invoices = picking_pool.action_invoice_create(
            self.env.cr,
            self.env.uid,
            pickings,
            self.journal_id.id, group=True,
            context={'ddt_partner_id': ddts[0].partner_invoice_id.id})
        invoice_obj = self.env['account.invoice'].browse(invoices)
        invoice_obj.write({
            'carriage_condition_id': ddts[0].carriage_condition_id.id,
            'goods_description_id': ddts[0].goods_description_id.id,
            'transportation_reason_id': ddts[0].transportation_reason_id.id,
            'transportation_method_id': ddts[0].transportation_method_id.id,
            'parcels': ddts[0].parcels,
            })
        for ddt in ddts:
            ddt.invoice_id = invoices[0]
        # ----- Show invoice
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
