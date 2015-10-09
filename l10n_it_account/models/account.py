# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Abstract srl (<http://www.abstract.it>)
#    Copyright (C) 2015 Agile Business Group sagl (<http://www.agilebg.com>)
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
##############################################################################

from openerp import fields, models, api

def set_acc_attrs(self, cr, uid, ids, context=None):
    if not context:
        context = {}
    account_model = self.pool['account.account']
    account_ids = account_model.search(
        cr, uid, [('change_bspl_side', '=', True)])

    for account in account_model.browse(cr, uid, account_ids, context=None):
        if not context:
            context = {}
        report_type = account.default_user_type.report_type
        balance = account.balance
        inverse_user_type = account.inverse_user_type
        inverse_parent_id = account.inverse_parent_id
        default_user_type = account.default_user_type
        default_parent_id = account.default_parent_id
        change_bspl_side = account.change_bspl_side

        if change_bspl_side:

            if report_type in ['asset', 'expense'] and balance < 0:
                account.user_type = inverse_user_type
                account.parent_id = inverse_parent_id
            elif report_type in ['asset', 'expense'] and balance >= 0:
                account.user_type = default_user_type
                account.parent_id = default_parent_id
            if report_type in ['liability', 'income'] and balance <= 0:
                account.user_type = default_parent_id
                account.parent_id = default_parent_id
            if report_type in ['liability', 'income'] and balance > 0:
                account.user_type = inverse_user_type
                account.parent_id = inverse_parent_id

class Report(models.Model):
    _inherit = 'report'

    def render(self, cr, uid, ids, template, values=None, context=None):
        if not context:
            context = {}
        res = super(Report, self).render(
            cr, uid, ids, template, values, context)
        set_acc_attrs(self, cr, uid, ids, context)
        return res

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def write(self, cr, uid, ids, vals, context=None, check=True,
            update_check=True):
        if not context:
            context = {}
        account_model = self.pool['account.account']
        res = super(AccountMoveLine, self).write(
            cr, uid, ids, vals, context, check, update_check)
        set_acc_attrs(self, cr, uid, ids, context)
        return res


class AccountAccount(models.Model):
    _inherit = 'account.account'

    change_bspl_side = fields.Boolean('Change BS/PL Side')
    default_user_type = fields.Many2one(
        'account.account.type',
        string='Default Account Type',
        help="Used on balance sheet to report this account when its balance \
        has standard sign")
    default_parent_id = fields.Many2one(
        'account.account',
        string='Default Parent',
        help="Used on balance sheet to report this account when its balance \
        has standard sign")
    inverse_user_type = fields.Many2one(
        'account.account.type',
        string='Inverse Account Type',
        help="Used on balance sheet to report this account when its balance \
        has opposite sign")
    inverse_parent_id = fields.Many2one(
        'account.account',
        string='Inverse Parent',
        help="Used on balance sheet to report this account when its balance \
        has opposite sign")
