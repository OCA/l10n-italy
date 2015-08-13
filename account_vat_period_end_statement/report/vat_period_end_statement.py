# -*- coding: utf-8 -*-
#
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-2012 Domsense s.r.l. (<http://www.domsense.com>).
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2015 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#    Copyright (C) 2015 Openforce di Alessandro Camilli
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
from openerp.osv import orm
from openerp.report import report_sxw
from openerp.tools.translate import _


class Report(orm.Model):
    _inherit = "report"


class vat_period_end_statement_report(report_sxw.rml_parse):
    _name = 'report.vat.period.end.statement'

    def __init__(self, cr, uid, name, context=None):
        if context is None:
            context = {}
        super(vat_period_end_statement_report, self).__init__(
            cr, uid, name, context=context)
        self.query = ""
        self.tot_currency = 0.0
        self.period_sql = ""
        self.sold_accounts = {}
        self.sortby = 'sort_date'
        self.localcontext.update({
            'time': time,
            'statement': self._get_statement,
            'tax_codes_amounts': self._get_tax_codes_amounts,
            'account_vat_amounts': self._get_account_vat_amounts,
        })
        self.context = context

    def _get_statement(self, statement_id):
        statement_obj = self.pool['account.vat.period.end.statement']
        statement = False
        if statement_id:
            statement = statement_obj.browse(
                self.cr, self.uid, statement_id, self.context)
        return statement

    def _compute_tax_amount(self, tax, tax_code, base_code, context=None):
        '''
        The Tax is child of another main tax.
        The main tax has more childs:
        - Child with tax_code_id are deductible
        - Child without tax_code_id are undeductible
        '''
        res = {}
        vat_deductible = 0
        vat_undeductible = 0
        vat_name = False
        if tax.parent_id:
            vat_code = tax.parent_id.description
            vat_name = tax.parent_id.name
            for child in tax.parent_id.child_ids:
                # deductibile
                if (
                    child.tax_code_id and
                    child.tax_code_id.vat_statement_account_id
                ):
                    vat_deductible = child.tax_code_id.sum_period
                # undeductibile
                else:
                    vat_undeductible = child.tax_code_id.sum_period
        else:
            vat_code = tax_code.code
            vat_name = tax_code.name
            vat_deductible = tax_code.sum_period

        res[vat_name] = {
            'code': vat_code,
            'tax_code_name': vat_name,
            'vat': vat_deductible + vat_undeductible,
            'vat_deductible': vat_deductible,
            'vat_undeductible': vat_undeductible,
            'base': base_code.sum_period
        }

        return res

    def _build_codes_dict(self, tax_code, res={}, context=None):

        if context is None:
            context = {}
        tax_pool = self.pool.get('account.tax')

        # search for taxes linked to that code
        tax_ids = tax_pool.search(
            self.cr, self.uid, [('tax_code_id', '=', tax_code.id)],
            context=context)
        if tax_ids:
            tax = tax_pool.browse(
                self.cr, self.uid, tax_ids[0], context=context)
            # search for the related base code
            base_code = (
                tax.base_code_id or tax.parent_id and
                tax.parent_id.base_code_id or False)
            if not base_code:
                raise orm.except_orm(
                    _('Error'),
                    _('No base code found for tax code %s') % tax_code.name)
            # check if every tax is linked to the same tax code and base code
            for tax in tax_pool.browse(
                self.cr, self.uid, tax_ids, context=context
            ):
                test_base_code = (
                    tax.base_code_id or tax.parent_id and
                    tax.parent_id.base_code_id or False)
                if test_base_code.id != base_code.id:
                    raise orm.except_orm(
                        _('Error'),
                        _('Not every tax linked to tax code %s is linked to '
                          'the same base code')
                        % tax_code.name)
            if tax_code.sum_period or base_code.sum_period:
                tax_vals = self._compute_tax_amount(
                    tax, tax_code, base_code, context)
                res.update(tax_vals)

        for child_code in tax_code.child_ids:
            res = self._build_codes_dict(
                child_code, res=res, context=context)

        return res

    def _get_tax_codes_amounts(self, period_id, tax_code_ids=[], context=None):
        if context is None:
            context = {}
        res = {}
        code_pool = self.pool.get('account.tax.code')
        context['period_id'] = period_id
        for tax_code in code_pool.browse(
            self.cr, self.uid, tax_code_ids, context=context
        ):
            res = self._build_codes_dict(tax_code, res=res, context=context)
        return res

    def _get_account_vat_amounts(
        self, type='credit', statement_account_line=[], context=None
    ):
        if context is None:
            context = {}
        if type != 'credit' and type != 'debit':
            raise orm.except_orm(
                _('Error'), _('Type account neither credit and debit !'))

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


class report_salecatalogbase(orm.AbstractModel):
    _name = ('report.account_vat_period_end_statement.'
             'report_vatperiodendstatement')
    _inherit = 'report.abstract_report'
    _template = 'account_vat_period_end_statement.report_vatperiodendstatement'
    _wrapped_report_class = vat_period_end_statement_report
