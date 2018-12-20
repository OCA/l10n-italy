# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Abstract (http://www.abstract.it)
#    Copyright (C) 2014 Agile Business Group (http://www.agilebg.com)
#    Copyright (C) 2015 Apulia Software s.r.l. (http://www.apuliasoftware.it)
#    @author Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
#    @author Giuseppe Stoduto
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
##############################################################################


from openerp import models, api, fields
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError


class DdTCreateInvoice(models.TransientModel):

    _inherit = "ddt.create.invoice"

    def _get_ddt_ids(self):
        return self.env['stock.picking.package.preparation'].browse(
            self.env.context['active_ids'])

    ddt_ids = fields.Many2many(
                'stock.picking.package.preparation', default=_get_ddt_ids)


    @api.multi
    def set_so_done(self, invoice_list):
        so_obj = self.env['sale.order']
        for invoice in invoice_list:
            so_ids = so_obj.search([('invoice_ids', '=', invoice)])
            for so_id in so_ids:
                if so_id.ddt_ids:
                    so_id.state = 'progress'

    @api.multi
    def create_invoice(self):
        ddt_model = self.env['stock.picking.package.preparation']
        picking_pool = self.pool['stock.picking']

        ddts = ddt_model.search(
            [('id', 'in', self.env.context['active_ids'])],
            order='partner_invoice_id')
        self.check_ddt_data(ddts)

        def _create_invoices(ddts):
            ddt_partner = {}
            for ddt in ddts:
                if ddt.partner_invoice_id.id in ddt_partner:
                    ddt_partner[ddt.partner_invoice_id.id].append(ddt)
                else:
                    ddt_partner[ddt.partner_invoice_id.id] = [ddt]

                for picking in ddt.picking_ids:
                    for move in picking.move_lines:
                        if move.invoice_state != "2binvoiced":
                            raise UserError(
                                _("Move {m} is not invoiceable ({d})".format(
                                    m=move.name, d=ddt.ddt_number)))
            invoice_list = []
            for partner_id in ddt_partner.keys():
                p_list = []
                # ---- Force to use partner invoice from ddt as invoice partner
                ctx = self.env.context.copy()
                ctx['ddt_partner_id'] = partner_id
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
                    'gross_weight': ddt_partner[partner_id][0].weight,
                    'net_weight': ddt_partner[partner_id][0].net_weight,
                    'volume': ddt_partner[partner_id][0].volume,
                })
                for ddt in ddt_partner[partner_id]:
                    ddt.invoice_id = invoices[0]
                invoice_list.append(invoices[0])
            return invoice_list

        invoice_list = []
        if self.group:
            invoice_list = _create_invoices(ddts)
        else:
            for ddt in ddts:
                invoice_list.append(_create_invoices([ddt]))

        self.set_so_done(invoice_list)
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
