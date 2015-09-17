# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2013 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#    Copyright (C) 2014 Agile Business Group sagl
#    (<http://www.agilebg.com>)
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
#

from openerp import models, fields, api


class AccountTaxCode(models.Model):
    _inherit = "account.tax.code"
    exclude_from_registries = fields.Boolean(
        string='Exclude from VAT registries')

    @api.one
    def sum_by_period_and_journals(self, period_id, journal_ids):
        # using self.id beacuse _sum returns
        # {tax_code_id: sum, child_tax_code_id: sum2, ...}
        return self._sum(
            False, False,
            where=" AND line.period_id=%s AND move.state='posted' "
                  "AND move.journal_id IN %s",
            where_params=(period_id, tuple(journal_ids)))[self.id]
