# -*- encoding: utf-8 -*-
#
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 Italian OpenERP Community
#    (<http://www.openerp-italia.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

from openerp.osv import orm, fields


class account_account(orm.Model):
    _inherit = "account.account"

    _columns = {
        'parent_consol_ids': fields.many2many(
            'account.account', 'account_account_consol_rel', 'parent_id',
            'child_id', 'Consolidated Parents'),
    }
