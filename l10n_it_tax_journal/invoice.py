# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>). 
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
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from report import report_sxw
from osv import osv
from tools.translate import _

class Parser(report_sxw.rml_parse):

    def _check_tax_code(self, tax_code):
        if not tax_code.tax_ids:
            raise Exception(_('No tax defined for tax code %s')
                % tax_code.code)
        if len(tax_code.tax_ids) > 1:
            raise Exception(_('Too many taxes defined for tax code %s')
                % tax_code.code)

    def _check_base_tax_code(self, tax_code):
        if not tax_code.base_tax_ids:
            raise Exception(_('No tax defined for tax code %s')
                % tax_code.code)
        if len(tax_code.base_tax_ids) > 1:
            raise Exception(_('Too many taxes defined for tax code %s')
                % tax_code.code)

    def _get_tax_lines(self, invoice):
        res=[]
        index=0
        for inv_tax in invoice.tax_line:
            if inv_tax.base_code_id and inv_tax.tax_code_id:
                self._check_tax_code(inv_tax.tax_code_id)
                tax_item = {
                    'tax_percentage': inv_tax.tax_code_id.tax_ids[0].amount and str(
                        inv_tax.tax_code_id.tax_ids[0].amount * 100).split('.')[0] or '',
                    'base': inv_tax.base,
                    'amount': inv_tax.amount,
                    'index': index,
                    }
                if inv_tax.amount == 0:
                    tax_item['amount']=inv_tax.tax_code_id.name
                res.append(tax_item)
                index += 1
            elif inv_tax.tax_code_id:
                self._check_tax_code(inv_tax.tax_code_id)
                tax_id = inv_tax.tax_code_id.tax_ids[0].id
                for inv_tax_2 in invoice.tax_line:
                    if inv_tax.base_code_id and not inv_tax.tax_code_id:
                        self._check_base_tax_code(inv_tax.base_code_id)
                        if inv_tax.base_code_id.base_tax_ids[0].id == tax_id:
                            tax_item = {
                                'tax_percentage': inv_tax.tax_code_id.tax_ids[0].amount and str(
                                    inv_tax.tax_code_id.tax_ids[0].amount * 100).split('.')[0] or '',
                                'base': inv_tax.base,
                                'amount': inv_tax.amount,
                                'index': index,
                                }
                            res.append(tax_item)
                            index += 1
                            break                
        return res

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
            'tax_lines': self._get_tax_lines,
        })
