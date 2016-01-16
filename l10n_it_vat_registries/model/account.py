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
    _inherit = "account.tax"
    exclude_from_registries = fields.Boolean(
        string='Exclude from VAT registries')

    @api.multi
    def _sum(self,  where ='', where_params=()):
        if self.env.context.get('based_on', 'invoices') == 'payments':
            self.env.cr.execute('SELECT line.tax_line_id, sum(line.debit - line.credit) \
                    FROM account_move_line AS line, \
                        account_move AS move \
                        LEFT JOIN account_invoice invoice ON \
                            (invoice.move_id = move.id) \
                    WHERE line.tax_line_id IN (%s) '+where+' \
                        AND move.id = line.move_id \
                        AND ((invoice.state = \'paid\') \
                            OR (invoice.id IS NULL)) \
                            GROUP BY line.tax_line_id',
                                (",".join([str(i.id) for i in self]),) + where_params)
        else:
            self.env.cr.execute('SELECT line.tax_line_id, sum(line.debit - line.credit) \
                    FROM account_move_line AS line, \
                    account_move AS move \
                    WHERE line.tax_line_id IN (%s) '+where+' \
                    AND move.id = line.move_id \
                    GROUP BY line.tax_line_id',
                       (",".join([str(i.id) for i in self]),) + where_params)
        res=dict(self.env.cr.fetchall())
        obj_precision = self.env['decimal.precision']
        res2 = {}
        for record in self:
            def _rec_get(record):
                amount = res.get(record.id) or 0.0
                return amount
            res2[record.id] = round(_rec_get(record), obj_precision.precision_get('Account'))
        return res2
    
    @api.one
    def sum_by_period_and_journals(self, from_date, to_date, journal_ids):
        # using self.id beacuse _sum returns
        # {tax_line_id: sum, child_tax_line_id: sum2, ...}
        return self._sum(
            where=" AND line.date>=%s AND line.date<=%s AND move.state='posted' "
                  "AND move.journal_id IN %s",
            where_params=(from_date, to_date, tuple(journal_ids)))[self.id]
