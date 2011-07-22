# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 Italian OpenERP Community (<http://www.openerp-italia.com>)                            
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
    
    
    # FIXME calcolare correttamente con tax inlcuded in price
    # TODO analizzare con tasse complesse che includono child taxes
    #
    def compute(self, cr, uid, invoice_id, context=None):
        tax_grouped = {}
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        inv = self.pool.get('account.invoice').browse(cr, uid, invoice_id, context=context)
        cur = inv.currency_id
        company_currency = inv.company_id.currency_id.id
        total_base = 0
        total_tax = {}
        total_amount_of_taxes_horizontal = 0
        number_deductible_account = 0
        for line in inv.invoice_line:
            # workout of total amount of taxes
            for tax in line.invoice_line_tax_id:
                key = tax['amount']
                if not key in total_tax:
                    # Total_tax 
                    total_tax[key] = [0]
                total_tax[key][0] += (line.price_unit* (1-(line.discount or 0.0)/100.0)) * tax['amount']
            for tax in tax_obj.compute_all(cr, uid, line.invoice_line_tax_id, (line.price_unit* (1-(line.discount or 0.0)/100.0)), line.quantity, inv.address_invoice_id.id, line.product_id, inv.partner_id)['taxes']:
                val={}
                val['invoice_id'] = inv.id
                val['name'] = tax['name']
                val['amount'] = tax['amount']
                val['price'] = (line.price_unit* (1-(line.discount or 0.0)/100.0)) * line.quantity
                val['manual'] = False
                val['sequence'] = tax['sequence']
                val['base'] = tax['price_unit'] * line['quantity']
                for line_tax in line.invoice_line_tax_id:
                    if tax["id"] == line_tax.id:
                        val['tax'] = [line_tax]                   
                total_base += val['base']

                if inv.type in ('out_invoice','in_invoice'):
                    val['base_code_id'] = tax['base_code_id']
                    val['tax_code_id'] = tax['tax_code_id']
                    val['base_amount'] = cur_obj.compute(cr, uid, inv.currency_id.id, company_currency, val['base'] * tax['base_sign'], context={'date': inv.date_invoice or time.strftime('%Y-%m-%d')}, round=False)
                    val['tax_amount'] = cur_obj.compute(cr, uid, inv.currency_id.id, company_currency, val['amount'] * tax['tax_sign'], context={'date': inv.date_invoice or time.strftime('%Y-%m-%d')}, round=False)
                    val['account_id'] = tax['account_collected_id'] or line.account_id.id
                else:
                    val['base_code_id'] = tax['ref_base_code_id']
                    val['tax_code_id'] = tax['ref_tax_code_id']
                    val['base_amount'] = cur_obj.compute(cr, uid, inv.currency_id.id, company_currency, val['base'] * tax['ref_base_sign'], context={'date': inv.date_invoice or time.strftime('%Y-%m-%d')}, round=False)
                    val['tax_amount'] = cur_obj.compute(cr, uid, inv.currency_id.id, company_currency, val['amount'] * tax['ref_tax_sign'], context={'date': inv.date_invoice or time.strftime('%Y-%m-%d')}, round=False)
                    val['account_id'] = tax['account_paid_id'] or line.account_id.id
                total_amount_of_taxes_horizontal += cur_obj.round(cr, uid, cur, val['tax_amount'])
                key = (val['tax_code_id'], val['base_code_id'], val['account_id'])
                if not key in tax_grouped:
                    tax_grouped[key] = val
                else:
                    tax_grouped[key]['amount'] += val['amount']
                    tax_grouped[key]['price'] += val['price']
                    tax_grouped[key]['base'] += val['base']
                    tax_grouped[key]['base_amount'] += val['base_amount']
                    tax_grouped[key]['tax_amount'] += val['tax_amount']

      
        index = 0
        for t in tax_grouped.values():
            t['base'] = cur_obj.round(cr, uid, cur, t['base'])
            t['amount'] = cur_obj.round(cr, uid, cur, t['amount'])
            t['base_amount'] = cur_obj.round(cr, uid, cur, t['base_amount'])
            
            # if it's a passive invoice change the deductible part
            # to make coincide total amount of taxes
            #if inv.type in ('in_invoice') and t['base_code_id'] != False:
            #    if 'tax' in t :
            #        total_tax[t['tax'][0]['amount']][1] += t['tax_amount']
            #    else:
            #        total_tax[t['parent_tax'][0]['amount']][1] += t['tax_amount']
            if inv.type in ('in_invoice') and t['base_code_id'] == False:
                number_deductible_account += 1 
            t['tax_amount'] = cur_obj.round(cr, uid, cur, t['tax_amount'])   
        total_amount_of_taxes_vertical = 0
        # round the total amount of taxes
        for t in total_tax.values():
            t[0] = cur_obj.round(cr, uid, cur, t[0])
            #t[1] = cur_obj.round(cr, uid, cur, t[1])
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

