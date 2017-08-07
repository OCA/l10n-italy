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

        ddts = ddt_model.search(
            [('id', 'in', self.env.context['active_ids'])],
            order='partner_invoice_id')
        ddt_partner = {}
        self.check_ddt_data(ddts)
        for ddt in ddts:
            if ddt.partner_invoice_id.id in ddt_partner:
                ddt_partner[ddt.partner_invoice_id.id].append(ddt)
            else:
                ddt_partner[ddt.partner_invoice_id.id] = [ddt]
            for picking in ddt.picking_ids:
                for move in picking.move_lines:
                    if move.invoice_state != "2binvoiced":
                        raise UserError(
                            _("Move {move} is not invoiceable ({ddt})".format(
                                move=move.name, ddt=ddt.ddt_number)))
        invoice_list = []
        for partner_id in ddt_partner.keys():
            p_list = []
            # ----- Force to use partner invoice from ddt as invoice partner
            ctx = self.env.context.copy()
            ctx['ddt_partner_id'] = partner_id  # ddts[0].partner_invoice_id.id
            ctx['inv_type'] = 'out_invoice'
            ctx['date_inv'] = self.date
            picking_list = [p.picking_ids for p in ddt_partner[partner_id]]
            for pll in picking_list:
                for p in pll:
                    p_list.append(p.id)
            invoices = picking_pool.action_invoice_create(
                self.env.cr,
                self.env.uid,
                p_list,  # pickings,
                self.journal_id.id, group=True,
                context=ctx)
            invoice_obj = self.env['account.invoice'].browse(invoices)
            invoice_obj.write({
                'carriage_condition_id': ddt_partner[
                    partner_id][0].carriage_condition_id.id,
                'goods_description_id': ddt_partner[
                    partner_id][0].goods_description_id.id,
                'transportation_reason_id': ddt_partner[
                    partner_id][0].transportation_reason_id.id,
                'transportation_method_id': ddt_partner[
                    partner_id][0].transportation_method_id.id,
                'parcels': ddt_partner[partner_id][0].parcels,
            })
            for ddt in ddt_partner[partner_id]:
                ddt.invoice_id = invoices[0]
            invoice_list.append(invoices[0])
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
            'res_ids': invoice_list,
            'view_id': False,
            'views': [(tree_id, 'tree'), (form_id, 'form')],
            'type': 'ir.actions.act_window',
            'domain': "[('type', '=', 'out_invoice'),"
                      " ('id','in', [" + ','.join(map(str, invoice_list)) +
                      "])]",
        }
