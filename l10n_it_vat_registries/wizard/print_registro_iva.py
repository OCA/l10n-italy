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

from odoo import models, fields, api, _
from odoo.exceptions import Warning as UserError


class WizardRegistroIva(models.TransientModel):
    _name = "wizard.registro.iva"

    from_date = fields.Date('From date', required=True)
    to_date = fields.Date('To date', required=True)
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
    message = fields.Char(string='Message', size=64, readonly=True)
    only_totals = fields.Boolean(
        string='Prints only totals')
    fiscal_page_base = fields.Integer('Last printed page', required=True)

    @api.onchange('tax_registry_id')
    def on_change_vat_registry(self):
        self.journal_ids = self.tax_registry_id.journal_ids
    
    def _build_contexts(self, data):
        result = {}
        result['journal_ids'] = 'journal_ids' in data['form'] and data['form']['journal_ids'] or False
        result['state'] = 'target_move' in data['form'] and data['form']['target_move'] or ''
        result['from_date'] = data['form']['from_date'] or False
        result['to_date'] = data['form']['to_date'] or False
        result['registry_type'] = data['form']['type'] or False
        result['fiscal_page_base'] = data['form']['fiscal_page_base'] or False
        #result['only_totals'] = data['only_totals'] or False
        return result
    
    def print_registro(self, data):
        wizard = self
        move_ids = self.env['account.move'].search([
            ('date', '>=', self.from_date),
            ('date', '<=', self.to_date),                               
            ('journal_id', 'in', [j.id for j in self.journal_ids]),
            ('state', '=', 'posted'),
            ], order='date, name')
        if not move_ids:
            raise UserError(_('No documents found in the current selection'))
        datas = {}
        datas_form = {}
        datas_form['from_date'] = wizard.from_date
        datas_form['to_date'] = wizard.to_date
        datas_form['journal_ids'] = [j.id for j in wizard.journal_ids]
        datas_form['fiscal_page_base'] = wizard.fiscal_page_base
        datas_form['registry_type'] = wizard.type
        list_id = []
        for move in move_ids:
            list_id.append(move.id)
        if wizard.tax_registry_id:
            datas_form['tax_registry_name'] = wizard.tax_registry_id.name
        else:
            datas_form['tax_registry_name'] = ''
        datas_form['only_totals'] = wizard.only_totals
        report_name = 'l10n_it_vat_registries.report_registro_iva'
        datas = {
            'ids': list_id,
            'model': 'account.move',
            'form': datas_form
        }
        print datas
        return self.env['report'].get_action([], report_name, data=datas)
    

        


 
