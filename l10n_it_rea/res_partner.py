# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Alessio Gerace <alessio.gerace@agilebg.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

from openerp import fields, models


class resPartner(models.Model):
    _inherit = 'res.partner'

    rea_office = fields.Many2one(
        'res.country.state', string='Office Province')
    rea_code = fields.Char('REA Code', size=20)
    rea_capital = fields.Float('Capital')
    rea_member_type = fields.Selection(
        [('SU', 'Unique Member'),
         ('SM', 'Multiple Members')], 'Member Type')
    rea_liquidation_state = fields.Selection(
        [('LS', 'In liquidation'),
         ('LN', 'Not in liquidation')], 'Liquidation State')

    _sql_constraints = [
        ('rea_code_uniq', 'unique (rea_code, company_id)',
         'The rea code code must be unique per company !'),
    ]
