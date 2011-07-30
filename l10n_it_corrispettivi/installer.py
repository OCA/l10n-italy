# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011 Associazione OpenERP Italia
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

from osv import fields, osv

class corrispettivi_config_data(osv.osv_memory):
    _name = 'corrispettivi.config.data'
    _inherit = 'res.config'

    _columns = {
        'default_credit_account_id': fields.many2one('account.account', 'Default credit account',
            domain=[('type','!=','view')], required=True, help='If doubtful, use income account'),
        'default_debit_account_id': fields.many2one('account.account', 'Default debit account',
            domain=[('type','!=','view')], required=True, help='If doubtful, use income account'),
        'journal_view_id': fields.many2one('account.journal.view', 'Journal View', required=True),
        }

    def execute(self, cr, uid, ids, context=None):
        for o in self.browse(cr, uid, ids, context=context):
            seq_id = self.pool.get('ir.sequence').create(cr, uid, {
                'name': 'Corrispettivi Journal',
                'code': 'account.journal',
                'padding': 3,
                'prefix': 'COJ/%(year)s/',
                })
            journal_id = self.pool.get('account.journal').create(cr, uid, {
                'view_id': o.journal_view_id.id,
                'code': 'COJ',
                'name': 'Corrispettivi Journal',
                'type': 'sale',
                'corrispettivi': True,
                'sequence_id': seq_id,
                'default_credit_account_id': o.default_credit_account_id.id,
                'default_debit_account_id': o.default_debit_account_id.id,
                })
            partner_id = self.pool.get('res.partner').create(cr, uid, {
                'name': 'Corrispettivi',
                'ref': 'COJ',
                'customer': False,
                'supplier': False,
                'corrispettivi': True,
                })
            address_id = self.pool.get('res.partner.address').create(cr, uid, {
                'name': 'Corrispettivi',
                'partner_id': partner_id,
                })

corrispettivi_config_data()

