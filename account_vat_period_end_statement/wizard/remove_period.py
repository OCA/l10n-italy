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

from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import UserError


class RemovePeriod(models.TransientModel):

    def _get_period_ids(self):
        statement_model = self.env['account.vat.period.end.statement']
        res = []
        if 'active_id' in self.env.context:
            statement = statement_model.browse(self.env.context['active_id'])
            for period in statement.date_range_ids:
                res.append((period.id, period.name))
        return res

    _name = 'remove.period.from.vat.statement'
    period_id = fields.Selection(_get_period_ids, 'Period', required=True)

    @api.multi
    def remove_period(self):
        self.ensure_one()
        if 'active_id' not in self.env.context:
            raise UserError(_('Current statement not found'))
        period = self.env['date.range'].browse(int(self.period_id))
        period.vat_statement_id = False
        statement = self.env['account.vat.period.end.statement'].browse(
            self.env.context['active_id'])
        statement.compute_amounts()
        return {
            'type': 'ir.actions.act_window_close',
        }
