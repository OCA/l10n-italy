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
        user_obj = self.pool.get('res.users')
        precision = self.pool.get('decimal.precision').precision_get(cr, uid, 'Account')
        if user_obj.browse(cr, uid, uid).company_id.vertical_comp:
            tax_obj = self.pool.get('account.tax')
            inv_obj = self.pool.get('account.invoice')

            inv = inv_obj.browse(cr, uid, invoice_id, context=context)

            for inv_tax in tax_grouped.values():
                inv_tax['tax_rate'] = tax_obj.get_main_tax(tax_obj.get_account_tax(cr, uid, inv_tax['name'])).amount
                inv_tax['tax_id'] = tax_obj.get_main_tax(tax_obj.get_account_tax(cr, uid, inv_tax['name'])).id

            tax_by_rate = {}
            # collect the base amount grouped by tax rate
            for line in inv.invoice_line:
                for tax in line.invoice_line_tax_id:
                    if not tax_by_rate.get(tax['amount'], False):
                        tax_by_rate[tax['amount']] = 0
                    tax_by_rate[tax['amount']] += round((line.price_unit* (1-(line.discount or 0.0)/100.0))
                        * line.quantity, precision)
            # compute the tax amount grouped by rate
            for rate in tax_by_rate:
                tax_by_rate[rate] = round(rate * tax_by_rate[rate], precision)

            # compute the tax amount of tax_grouped, grouped by tax rate
            wrong_tax_by_rate = {}
            for inv_tax in tax_grouped.values():
                if not wrong_tax_by_rate.get(inv_tax['tax_rate'], False):
                    wrong_tax_by_rate[inv_tax['tax_rate']] = 0
                wrong_tax_by_rate[inv_tax['tax_rate']] += inv_tax['tax_amount']

            difference_by_rate = {}
            for rate in tax_by_rate:
                difference_by_rate[rate] = tax_by_rate[rate] - wrong_tax_by_rate[rate]

            for rate in difference_by_rate:
                value_set = False
                # first try to add difference to non deductible tax
                for inv_tax in tax_grouped.values():
                    if inv_tax['tax_rate'] == rate:
                        if inv_tax['base_code_id'] == False:
                            inv_tax['tax_amount'] =  inv_tax['tax_amount'] + difference_by_rate[rate]
                            inv_tax['amount'] =  inv_tax['amount'] + difference_by_rate[rate]
                            value_set = True
                            break
                # else add it to the normal tax
                if not value_set:
                    for inv_tax in tax_grouped.values():
                        if inv_tax['tax_rate'] == rate:
                            inv_tax['tax_amount'] =  inv_tax['tax_amount'] + difference_by_rate[rate]
                            inv_tax['amount'] =  inv_tax['amount'] + difference_by_rate[rate]
                            value_set = True
                            break

        return tax_grouped
    
account_invoice_tax()    

