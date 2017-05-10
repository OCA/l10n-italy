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


class AddPeriod(models.TransientModel):

    _name = 'add.period.to.vat.statement'
    period_id = fields.Many2one(
        'date.range', 'Period', required=True)

    @api.multi
    def add_period(self):
        self.ensure_one()
        if 'active_id' not in self.env.context:
            raise UserError(_('Current statement not found'))
        statement_env = self.env['account.vat.period.end.statement']
        wizard = self
        if wizard.period_id.vat_statement_id:
            raise UserError(
                _('Period %s is associated to statement %s yet') %
                (
                    wizard.period_id.name,
                    wizard.period_id.vat_statement_id.date)
            )
        statement_id = self.env.context['active_id']
        wizard.period_id.vat_statement_id = statement_id
        statement = statement_env.browse(statement_id)
        statement.compute_amounts()
        return {
            'type': 'ir.actions.act_window_close',
        }
