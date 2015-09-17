# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2011 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#    Copyright (C) 2014-2015 Agile Business Group
#    (<http://www.agilebg.com>)
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
from openerp.exceptions import Warning as UserError


class WizardRegistroIva(models.TransientModel):

    @api.model
    def _get_period(self):
        ctx = dict(self._context or {}, account_period_prefer_normal=True)
        period_ids = self.env[
            'account.period'].with_context(context=ctx).find()
        return period_ids

    _name = "wizard.registro.iva"
    _rec_name = "type"

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
    tax_registry_id = fields.Many2one('account.tax.registry', 'VAT registry')
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
    only_totals = fields.Boolean(
        string='Prints only totals')
    fiscal_page_base = fields.Integer('Last printed page', required=True)

    @api.onchange('tax_registry_id')
    def on_change_vat_registry(self):
        self.journal_ids = self.tax_registry_id.journal_ids
        self.type = self.tax_registry_id.type
        if self.type:
            if self.type == 'supplier':
                self.tax_sign = -1
            else:
                self.tax_sign = 1

    def print_registro(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids[0], context=context)
        move_obj = self.pool['account.move']
        move_ids = move_obj.search(cr, uid, [
            ('journal_id', 'in', [j.id for j in wizard.journal_ids]),
            ('period_id', 'in', [p.id for p in wizard.period_ids]),
            ('state', '=', 'posted'),
            ], order='date, name')
        if not move_ids:
            raise UserError(_('No documents found in the current selection'))
        datas = {}
        datas_form = {}
        datas_form['period_ids'] = [p.id for p in wizard.period_ids]
        datas_form['journal_ids'] = [j.id for j in wizard.journal_ids]
        datas_form['tax_sign'] = wizard.tax_sign
        datas_form['fiscal_page_base'] = wizard.fiscal_page_base
        datas_form['registry_type'] = wizard.type
        if wizard.tax_registry_id:
            datas_form['tax_registry_name'] = wizard.tax_registry_id.name
        else:
            datas_form['tax_registry_name'] = ''
        datas_form['only_totals'] = wizard.only_totals
        report_name = 'l10n_it_vat_registries.report_registro_iva'
        datas = {
            'ids': move_ids,
            'model': 'account.move',
            'form': datas_form
        }
        return self.pool['report'].get_action(
            cr, uid, [], report_name, data=datas, context=context)

    @api.onchange('type')
    def on_type_changed(self):
        if self.type:
            if self.type == 'supplier':
                self.tax_sign = -1
            else:
                self.tax_sign = 1
