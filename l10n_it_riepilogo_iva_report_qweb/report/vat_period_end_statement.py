# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Andre@ (<a.gallina@cgsoftware.it>)
#    All Rights Reserved
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

import time
from openerp.report import report_sxw
from openerp.tools.translate import _
from openerp import api, models
from openerp.osv import orm


class VatPeriodEndStatement(models.AbstractModel):
    _name = 'report.l10n_it_riepilogo_iva_report_qweb.vat_period_end_statement'

    def _build_codes_dict(self, tax_code, period_id=False, res={}):
        tax_pool = self.env['account.tax'].with_context(period_id=period_id)
        if tax_code.sum_period:
            #~ if res.get(tax_code.name, False):
                #~ raise orm.except_orm(
                    #~ _('Error'),
                    #~ _('Too many occurences of tax code %s') % tax_code.name)
            # search for taxes linked to that code
            tax_ids = tax_pool.search([('tax_code_id', '=', tax_code.id)])
            if tax_ids:
                tax = tax_ids[0]
                # search for the related base code
                base_code = tax.base_code_id or tax.parent_id \
                    and tax.parent_id.base_code_id or False
                if not base_code:
                    raise orm.except_orm(
                        _('Error'),
                        _('No base code found for tax code %s') % tax_code.name)
                # check if every tax is linked to the same tax code and base code
                #~ for tax in tax_ids:
                    #~ test_base_code = tax.base_code_id or tax.parent_id \
                        #~ and tax.parent_id.base_code_id or False
                    #~ if test_base_code.id != base_code.id:
                        #~ raise orm.except_orm(
                            #~ _('Error'),
                            #~ _('Not every tax linked to tax code '\
                              #~ '%s is linked the same base code')
                              #~ % tax_code.name)
                if not tax_code.name in res:
                    res[tax_code.name] = {
                        'code': tax_code.code or '',
                        'vat': tax_code.sum_period * tax_code.vat_statement_sign,
                        'base': base_code.sum_period * base_code.vat_statement_sign,
                        }
                else:
                    res[tax_code.name]['vat'] += tax_code.sum_period * tax_code.vat_statement_sign
                    res[tax_code.name]['base'] += base_code.sum_period * base_code.vat_statement_sign
            for child_code in tax_code.child_ids:
                res = self._build_codes_dict(child_code, res=res)
        return res
    
    def _get_tax_codes_amounts(self, period_ids, tax_code_ids=[]):
        res = {}
        for period_id in period_ids:
            code_pool = self.env['account.tax.code'].with_context(
                period_id=period_id)
            for tax_code in code_pool.browse(tax_code_ids):
                res = self._build_codes_dict(tax_code, period_id=period_id,
                                             res=res)
        return res or {}

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(
            'l10n_it_riepilogo_iva_report_qweb.vat_period_end_statement')
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'o': self.env[report.model].browse(self._ids),
            'tax_codes_amounts': self._get_tax_codes_amounts,
        }
        return report_obj.render(
            'l10n_it_riepilogo_iva_report_qweb.vat_period_end_statement',
            docargs)
