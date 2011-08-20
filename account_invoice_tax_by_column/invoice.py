# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011
#    Associazione OpenERP Italia (<http://www.openerp-italia.org>)
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
from osv import fields, osv


class account_invoice_tax(osv.osv):
    _inherit = "account.invoice.tax"

    def compute(self, cr, uid, invoice_id, context=None):
        tax_grouped = super(account_invoice_tax, self).compute(cr, uid, invoice_id, context)
        total_base = 0
        total_tax = {}
        total_amount_of_taxes_horizontal = 0
        number_deductible_account = 0
        cur_obj = self.pool.get('res.currency')
        inv = self.pool.get('account.invoice').browse(cr, uid, invoice_id, context=context)
        cur = inv.currency_id
        for line in inv.invoice_line:
            # workout of total amount of taxes
            for tax in line.invoice_line_tax_id:
                key = tax['amount']
                if not key in total_tax:
                    # Total_tax 
                    total_tax[key] = [0]
                total_tax[key][0] += (line.price_unit* (1-(line.discount or 0.0)/100.0)) * tax['amount']

        index = 0
        for t in tax_grouped.values():
            if inv.type in ('in_invoice') and t['base_code_id'] == False:
                number_deductible_account += 1 
            total_amount_of_taxes_horizontal += t['tax_amount']

        total_amount_of_taxes_vertical = 0
        # round the total amount of taxes
        for t in total_tax.values():
            t[0] = cur_obj.round(cr, uid, cur, t[0])
            total_amount_of_taxes_vertical += t[0]
        total_amount_of_taxes_vertical = cur_obj.round(cr, uid, cur, total_amount_of_taxes_vertical)
        total_amount_of_taxes_horizontal = cur_obj.round(cr, uid, cur, total_amount_of_taxes_horizontal)
        if number_deductible_account != 0:
            quotient = (total_amount_of_taxes_vertical - total_amount_of_taxes_horizontal) / number_deductible_account
            quotient = cur_obj.round(cr, uid, cur, quotient)
            remainder = (total_amount_of_taxes_vertical - total_amount_of_taxes_horizontal) - number_deductible_account * quotient
            remainder = cur_obj.round(cr, uid, cur, remainder)
        # change at least a deductible tax amount to to make coincide total amount of taxes
        counter = 0
        if inv.type in ('in_invoice') and total_amount_of_taxes_vertical != total_amount_of_taxes_horizontal:
            for t in tax_grouped.values():               
                if t['base_code_id'] == False:
                    counter += 1
                    t['tax_amount'] =  t['tax_amount'] + quotient
                    t['amount'] =  t['amount'] + quotient
                    if counter == number_deductible_account:
                        t['tax_amount'] =  t['tax_amount'] + remainder
                        t['amount'] =  t['amount'] + remainder  
        return tax_grouped
    
account_invoice_tax()    

