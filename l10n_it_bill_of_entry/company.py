# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2013 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2013
#    Associazione OpenERP Italia (<http://www.openerp-italia.org>)
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

from openerp.osv import fields, orm


class res_company(orm.Model):
    _inherit = 'res.company'
    _columns = {
        'bill_of_entry_journal_id': fields.many2one(
            'account.journal', 'Bill of entry Storno journal',
            help="Journal used for reconciliation of customs supplier"),
    }


class account_config_settings(orm.TransientModel):
    _inherit = 'account.config.settings'
    _columns = {
        'bill_of_entry_journal_id': fields.related(
            'company_id', 'bill_of_entry_journal_id',
            type='many2one',
            relation="account.journal",
            string="Bill of entry Storno journal",
            help='Journal used for reconciliation of customs supplier'),
    }
