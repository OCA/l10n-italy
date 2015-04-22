# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Abstract (http://www.abstract.it)
#    Author: Davide Corio <davide.corio@abstract.it>
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

from openerp import pooler, models, fields
from openerp.osv import fields as oldfields


class One2manyFiltered(oldfields.one2many):

    def get(self, cr, obj, ids, name, user=None, offset=0, context=None,
            values=None):
        uid = context.get('uid')
        move_line_model = pooler.get_pool(cr.dbname)['account.move.line']
        user_model = pooler.get_pool(cr.dbname)['res.users']
        company = user_model.browse(cr, uid, uid).company_id
        res = super(One2manyFiltered, self).get(
            cr, obj, ids, name, user=user, offset=offset, context=context,
            values=values)
        if company.enable_skip_move_line and company.skip_move_line_expr and\
                eval(company.skip_move_line_expr):
            for move_id in res:
                line_ids = res[move_id]
                for line in move_line_model.browse(
                        cr, uid, line_ids, context=context):
                    if line.skip:
                        line_ids.remove(line.id)
                res[move_id] = line_ids
        return res


class AccountMove(models.Model):
    _inherit = 'account.move'

    _columns = {
        'line_id': One2manyFiltered(
            'account.move.line',
            'move_id',
            'Entries',
            states={'posted': [('readonly', True)]},
            copy=True),
        }

    def write(self, cr, uid, ids, values, context=None):
        if not context:
            context = {}
        for line in values['line_id']:
            if line[2] and not line[2]['credit'] and not line[2]['debit']:
                line[2]['skip'] = True
        return super(AccountMove, self).write(
            cr, uid, ids, values, context=context)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    skip = fields.Boolean('Skip')

    def write(
            self, cr, uid, ids, values, context=None, check=True,
            update_check=True):
        if not context:
            context = {}
        import ipdb;ipdb.set_trace()
        return super(AccountMoveLine, self).write(
            cr, uid, ids, values, context=context, check=check,
            update_check=update_check)
