# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-2012 Domsense s.r.l. (<http://www.domsense.com>).
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
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
##############################################################################

import time
from report import report_sxw
from tools.translate import _

class print_vat_period_end_statement(report_sxw.rml_parse):
    _name = 'parser.vat.period.end.statement'
    
    def _build_codes_dict(self, tax_code, res={}, context=None):
        if context is None:
            context = {}
        tax_pool = self.pool.get('account.tax')
        if tax_code.sum_period:
            if res.get(tax_code.name, False):
                raise osv.except_osv(_('Error'), _('Too many occurences of tax code %s') % tax_code.name)
            # search for taxes linked to that code
            tax_ids = tax_pool.search(self.cr, self.uid, [('tax_code_id', '=', tax_code.id)], context=context)
            if tax_ids:
                tax = tax_pool.browse(self.cr, self.uid, tax_ids[0], context=context)
                # search for the related base code
                base_code = tax.base_code_id or tax.parent_id and tax.parent_id.base_code_id or False
                if not base_code:
                    raise osv.except_osv(_('Error'), _('No base code found for tax code %s') % tax_code.name)
                # check if every tax is linked to the same tax code and base code
                for tax in tax_pool.browse(self.cr, self.uid, tax_ids, context=context):
                    test_base_code = tax.base_code_id or tax.parent_id and tax.parent_id.base_code_id or False
                    if test_base_code.id != base_code.id:
                        raise osv.except_osv(_('Error'), _('Not every tax linked to tax code %s is linked the same base code') % tax_code.name)
                res[tax_code.name] = {
                    'vat': tax_code.sum_period,
                    'base': base_code.sum_period,
                    }
            for child_code in tax_code.child_ids:
                res = self._build_codes_dict(child_code, res=res, context=context)
        return res
    
    def _get_tax_codes_amounts(self, period_id, tax_code_ids=[], context=None):
        if context is None:
            context = {}
        res = {}
        code_pool = self.pool.get('account.tax.code')
        context['period_id'] = period_id
        for tax_code in code_pool.browse(self.cr, self.uid, tax_code_ids, context=context):
            res = self._build_codes_dict(tax_code, res=res, context=context)
        return res
    
    def find_period(self, date,context=None):
        if context is None:
            context = {}
        period_pool = self.pool.get('account.period')
        period_ids = period_pool.find(self.cr, self.uid, dt=date, context=context)
        if len(period_ids)> 1:
            raise osv.except_osv(_('Error'), _('Too many periods for date %s') % str(date))
        return period_ids[0]
        
    def __init__(self, cr, uid, name, context=None):
        if context is None:
            context = {}
        super(print_vat_period_end_statement, self).__init__(cr, uid, name, context=context)
        self.localcontext.update( {
            'time': time,
            'tax_codes_amounts': self._get_tax_codes_amounts,
            'find_period': self.find_period,
        })
        self.context = context

report_sxw.report_sxw('report.account.print.vat.period.end.statement',
                      'account.vat.period.end.statement',
                      'addons/account_vat_period_end_statement/report/vat_period_end_statement.mako',
                      parser=print_vat_period_end_statement)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
