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

from datetime import datetime

from odoo import _, api, fields, models


class AccountVatPeriodEndStatement(models.Model):
    _inherit = 'account.vat.period.end.statement'

    @api.multi
    def compute_amounts(self):
        res = super(AccountVatPeriodEndStatement, self).compute_amounts()

        for statement in self:

            statement.generic_vat_account_line_ids = \
                statement.generic_vat_account_line_ids.filtered(
                    lambda x: not x.is_split_payment)

            for date_range in statement.date_range_ids:
                acc_move_line_obj = self.env['account.move.line']
                domain = [('invoice_id.amount_sp', '!=', 0.0),
                          ('tax_line_id', '!=', False),
                          ('date', '>=', date_range.date_start),
                          ('date', '<=', date_range.date_end)]
                acc_move_lines = acc_move_line_obj.search(domain)

                if not acc_move_lines:
                    continue
                grouped_lines = acc_move_lines.group_by_account_and_tax()

                generic_line_obj = self.env['statement.generic.account.line']
                date_start = datetime.strptime(date_range.date_start, '%Y-%m-%d')
                date_start_str = datetime.strftime(date_start, '%d-%m-%Y')
                date_end = datetime.strptime(date_range.date_end, '%Y-%m-%d')
                date_end_str = datetime.strftime(date_end, '%d-%m-%Y')

                for group_key in grouped_lines:
                    account_id = group_key[0].id

                    amount = 0.0
                    for line in grouped_lines[group_key]:
                        amount += line.credit - line.debit

                    is_split_payment = True

                    if self.env.user.company_id \
                     and self.env.user.company_id.sp_description:
                        name = self.env.user.company_id.sp_description
                    else:
                        name = _("Write-off tax amount on tax ")

                    name += _("{} - from {} to {}".format(group_key[1].description, date_start_str, date_end_str))

                    statement_id = statement.id

                    generic_line_vals = {
                        'account_id': account_id,
                        'amount': amount,
                        'is_split_payment': is_split_payment,
                        'name': name,
                        'statement_id': statement_id
                    }
                    generic_line_obj.create(generic_line_vals)

        return res


class StatementGenericAccountLine(models.Model):
    _inherit = 'statement.generic.account.line'

    is_split_payment = fields.Boolean()
