# -*- coding: utf-8 -*-
#
##############################################################################
#
#    Author(s): Silvio Gregorini (silviogregorini@openforce.it)
#
#    Copyright © 2018 Openforce Srls Unipersonale (www.openforce.it)
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
#    along with this program. If not, see:
#    http://www.gnu.org/licenses/agpl-3.0.txt.
#
##############################################################################

from odoo import _, api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.multi
    def group_by_account_and_tax(self):

        grouped_lines = {}

        for line in self:
            group_key = (line.account_id, line.tax_line_id)
            if group_key not in grouped_lines:
                grouped_lines.update({group_key: []})
            grouped_lines[group_key].append(line)

        return grouped_lines
