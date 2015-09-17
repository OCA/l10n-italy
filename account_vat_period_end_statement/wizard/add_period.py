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


class AddPeriod(orm.TransientModel):

    _name = 'add.period.to.vat.statement'

    _columns = {
        'period_id': fields.many2one(
            'account.period', 'Period', required=True),
    }

    def add_period(self, cr, uid, ids, context=None):
        if 'active_id' not in context:
            raise orm.except_orm(_('Error'), _('Current statement not found'))
        statement_pool = self.pool.get('account.vat.period.end.statement')
        wizard = self.browse(cr, uid, ids, context)[0]
        if wizard.period_id.vat_statement_id:
            raise orm.except_orm(
                _('Error'), _('Period %s is associated to statement %s yet') %
                (wizard.period_id.name, wizard.period_id.vat_statement_id.date)
            )
        wizard.period_id.write({'vat_statement_id': context['active_id']})
        statement_pool.compute_amounts(
            cr, uid, [context['active_id']], context=context)
        return {
            'type': 'ir.actions.act_window_close',
        }
