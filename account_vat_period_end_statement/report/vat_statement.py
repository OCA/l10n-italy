# -*- coding: utf-8 -*-
#
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-2012 Domsense s.r.l. (<http://www.domsense.com>).
#    Copyright (C) 2012-2017 Agile Business Group (<http://www.agilebg.com>)
#    Copyright (C) 2015 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#    Copyright (C) 2015 Openforce di Alessandro Camilli
#    Copyright (C) 2015 Link It S.p.a. (<http://www.linkgroup.it/>)
#    <http://www.openforce.it>
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

import time
from odoo import models, api
from odoo.tools.translate import _
from odoo.tools.misc import formatLang


class VatPeriodEndStatementReport(models.AbstractModel):
    _name = 'report.account_vat_period_end_statement.vat_statement'

    @api.model
    def render_html(self, docids, data=None):
        docs = self.env['account.vat.period.end.statement'].browse(docids)
        docargs = {
            'docs': docs,
            'time': time,
            'tax_amounts': self._get_taxes_amounts,
            'account_vat_amounts': self._get_account_vat_amounts,
            'formatLang': formatLang,
            'env': self.env,
        }
        return self.env['report'].render(
            'account_vat_period_end_statement.vat_statement', docargs)

    def _get_statement(self, statement_id):
        statement_obj = self.env['account.vat.period.end.statement']
        statement = False
        if statement_id:
            statement = statement_obj.browse(statement_id)
        return statement

    def _get_taxes_amounts(
        self, period_id, tax_ids=None, registry_type='customer'
    ):
        if tax_ids is None:
            tax_ids = []
        res = {}
        date_range = self.env['date.range'].browse(period_id)
        tax_model = self.env['account.tax']

        for tax_id in tax_ids:
            tax = tax_model.browse(tax_id)
            tax_name, base, tax_val, deductible, undeductible = (
                tax._compute_totals_tax({
                    'from_date': date_range.date_start,
                    'to_date': date_range.date_end,
                    'registry_type': registry_type,
                })
            )

            if (
                tax.cee_type and tax.parent_tax_ids and
                len(tax.parent_tax_ids) == 1
            ):
                # In caso di integrazione iva l'imponibile è solo sulla
                # padre
                parent = tax.parent_tax_ids[0]

                tax_data = parent._compute_totals_tax({
                    'from_date': date_range.date_start,
                    'to_date': date_range.date_end,
                    'registry_type': registry_type,
                    })
                # return tax_name, base, tax_val, deductible, undeductible
                base = tax_data[1]

            res[tax_name] = {
                'code': tax_name,
                'vat': tax_val,
                'vat_deductible': deductible,
                'vat_undeductible': undeductible,
                'base': base
            }
        return res

    def _get_account_vat_amounts(
        self, type='credit', statement_account_line=None,
    ):
        if statement_account_line is None:
            statement_account_line = []
        if type != 'credit' and type != 'debit':
            raise Exception(_('Account type neither credit and debit !'))

        account_amounts = {}
        for line in statement_account_line:
            account_id = line.account_id.id
            if account_id not in account_amounts:
                account_amounts[account_id] = {
                    'account_id': line.account_id.id,
                    'account_name': line.account_id.name,
                    'amount': line.amount
                }
            else:
                account_amounts[account_id]['amount'] += line.amount
        return account_amounts
