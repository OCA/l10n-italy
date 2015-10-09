# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2011-2012 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#    All Rights Reserved
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
##############################################################################

# from osv import fields, osv
from openerp import fields
from openerp import models
from openerp import api


class account_report_prima_nota_cassa(models.TransientModel):
    _inherit = "account.common.account.report"
    _name = 'account.report.prima_nota_cassa'
    _description = "Print Prima Nota Cassa"

    @api.multi
    def _get_all_journal(self):
        return self.env['account.journal'].search([
            ('type', 'in', ['cash', 'bank'])])

    def _print_report(self, cr, uid, ids, data, context=None):
        if context is None:
            context = {}
        data = self.pre_print_report(cr, uid, ids, data, context=context)
        data['form'].update(self.read(cr, uid, ids, ['landscape', 'initial_balance', 'amount_currency', 'sortby'])[0])
        # GTK client problem onchange does not consider in save record
        if not data['form']['fiscalyear_id']:
            data['form'].update({'initial_balance': False})
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'l10n_it_prima_nota_cassa.report_primanotacassa',
            'datas': data
        }

    initial_balance = fields.Boolean(
        'Include initial balances',
        help="""It adds initial balance row on report which display previous
sum amount of debit/credit/balance""")

    _defaults = {
        'journal_ids': _get_all_journal,
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
