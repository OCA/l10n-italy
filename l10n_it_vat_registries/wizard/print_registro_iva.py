# -*- encoding: utf-8 -*-
#
#
#    Copyright (C) 2011 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

from openerp import models, fields, api, _

class wizard_registro_iva(models.TransientModel):

    @api.model
    def _get_period(self):
        ctx = dict(self._context or {}, account_period_prefer_normal=True)
        period_ids = self.env[
            'account.period'].find(self._cr, self.env.user, context=ctx)
        return period_ids

    _name = "wizard.registro.iva"

    period_ids = fields.Many2many(
        'account.period',
        'registro_iva_periods_rel',
        'period_id',
        'registro_id',
        string='Periods',
        default=_get_period,
        help='Select periods you want retrieve documents from',
        required=True)
    type = fields.Selection([
        ('customer', 'Customer Invoices'),
        ('supplier', 'Supplier Invoices'),
        ('corrispettivi', 'Corrispettivi'),
        ], 'Layout', required=True,
        default='customer')
    journal_ids = fields.Many2many(
        'account.journal',
        'registro_iva_journals_rel',
        'journal_id',
        'registro_id',
        string='Journals',
        help='Select journals you want retrieve documents from',
        required=True)
    tax_sign = fields.Float(
        string='Tax amount sign',
        default=1.0,
        help="Use -1 you have negative tax \
        amounts and you want to print them prositive")
    message = fields.Char(string='Message', size=64, readonly=True)
    fiscal_page_base = fields.Integer(
        string='Last printed page',
        default=0,
        required=True)

    @api.one
    def print_registro(self):
        move_obj = self.env('account.move')
        obj_model_data = self.env('ir.model.data')
        move_ids = move_obj.search([
            ('journal_id', 'in', [j.id for j in self.journal_ids]),
            ('period_id', 'in', [p.id for p in self.period_ids]),
            ('state', '=', 'posted'),
            ], order='date, name')
        if not move_ids:
            self.message = _('No documents found in the current selection')
            model_data_ids = obj_model_data.search(
                [('model', '=', 'ir.ui.view'),
                 ('name', '=', 'wizard_registro_iva')])
            resource_id = obj_model_data.read(
                self._cr,
                self.env,
                model_data_ids,
                fields=['res_id'])[0]['res_id']
            return {
                'name': _('No documents'),
                'res_id': self.id,
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'wizard.registro.iva',
                'views': [(resource_id, 'form')],
                'context': self._context,
                'type': 'ir.actions.act_window',
                'target': 'new',
            }
        datas = {'ids': move_ids}
        datas['model'] = 'account.move'
        datas['fiscal_page_base'] = self.fiscal_page_base
        datas['period_ids'] = [p.id for p in self.period_ids]
        datas['layout'] = self.type
        datas['tax_sign'] = self.tax_sign
        res = {
            'type': 'ir.actions.report.xml',
            'datas': datas,
        }
        if self.type == 'customer':
            res['report_name'] = 'registro_iva_vendite'
        elif self.type == 'supplier':
            res.report_name = 'registro_iva_acquisti'
        elif self.type == 'corrispettivi':
            res['report_name'] = 'registro_iva_corrispettivi'
        return res

    @api.onchange('type')
    def on_type_changed(self):
        if self.type:
            if self.type == 'supplier':
                self.tax_sign = -1
            else:
                self.tax_sign = 1
