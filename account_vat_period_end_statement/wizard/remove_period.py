# -*- coding: utf-8 -*-
#
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 Domsense s.r.l. (<http://www.domsense.com>).
#    Copyright (C) 2012-15 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2015 Associazione Odoo Italia
#    (<http://www.odoo-italia.org>).
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
from openerp.tools.translate import _


class RemovePeriod(orm.TransientModel):

    def _get_period_ids(self, cr, uid, context=None):
        statement_obj = self.pool.get('account.vat.period.end.statement')
        res = []
        if 'active_id' in context:
            statement = statement_obj.browse(
                cr, uid, context['active_id'], context)
            for period in statement.period_ids:
                res.append((period.id, period.name))
        return res

    _name = 'remove.period.from.vat.statement'

    _columns = {
        'period_id': fields.selection(
            _get_period_ids, 'Period', required=True),
    }

    def remove_period(self, cr, uid, ids, context=None):
        if 'active_id' not in context:
            raise orm.except_orm(_('Error'), _('Current statement not found'))
        self.pool.get('account.period').write(
            cr, uid, [int(self.browse(cr, uid, ids, context)[0].period_id)],
            {'vat_statement_id': False}, context=context)
        self.pool.get('account.vat.period.end.statement').compute_amounts(
            cr, uid, [context['active_id']], context=context)
        return {
            'type': 'ir.actions.act_window_close',
        }
