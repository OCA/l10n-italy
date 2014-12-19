# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Abstract (http://www.abstract.it)
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


class DdTCreateInvoice(models.TransientModel):

    _name = "ddt.create.invoice"

    journal_id = fields.Many2one('account.journal', 'Journal')
    date = fields.Date('Date')

    def _prepare_invoice_line(self, invoice, move):
        invoice_line_data = {
            'invoice_id': invoice.id,
            'product_id': move.product_id.id,
            'name': move.name,
        }
        return invoice_line_data

    @api.multi
    def create_invoice(self):
        wizard = self[0]
        ddt_model = self.env['stock.ddt']
        invoice_model = self.env['account.invoice']
        invoice_line_model = self.env['account.invoice.line']

        ddts = ddt_model.browse(self.env.context['active_ids'])
        partners = set([ddt.partner_id for ddt in ddts])
        partner = list(partners)[0]

        invoice_data = {
            'partner_id': partner.id,
            'date_invoice': wizard.date,
            'journal_id': wizard.journal_id.id,
            'account_id': partner.property_account_receivable.id,
        }

        invoice = invoice_model.create(invoice_data)

        for ddt in ddts:
            for picking in ddt.picking_ids:
                for move in picking.move_lines:
                    invoice_line_data = self._prepare_invoice_line(
                        invoice, move)
                    invoice_line_model.create(invoice_line_data)

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
            'res_id': invoice.id,
            'view_id': False,
            'views': [(form_id, 'form'), (tree_id, 'tree')],
            'type': 'ir.actions.act_window',
        }
