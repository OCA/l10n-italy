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

    def compute_taxes_by_rate(self, cr, uid, lines=[], precision=2, address_id=None, partner=None):

        # lines has the form
        # [{'price_unit': 100, 'discount': 0, 'quantity': 1, 'taxes': [account.tax], 'product': product.product}]
        # returns a dictionary like {0.2: 20}

        tax_obj = self.pool.get('account.tax')
        tax_by_rate = {}
        # collect the base amount grouped by tax rate
        for line in lines:
            for tax in line['taxes']:
                # TODO manage multi currency
                if not tax_by_rate.get(tax['id'], False):
                    tax_by_rate[tax['id']] = {'base_amount': 0.0, 'product': None}
                tax_by_rate[tax['id']]['base_amount'] += (line['price_unit'] * (1-(line['discount'] or 0.0)/100.0)) \
                    * line['quantity']
                if line.get('product', False):
                    tax_by_rate[tax['id']]['product']  = line['product']
        # compute the tax amount grouped by tax
        for tax_id in tax_by_rate:
            tax = tax_obj.browse(cr, uid, tax_id)
            total = tax_obj.compute_all(cr, uid, [tax], tax_by_rate[tax_id]['base_amount'], 1,
                address_id=address_id, product=tax_by_rate[tax_id]['product'], partner=partner)
            tax_by_rate[tax_id] = total['total_included'] - total['total']

        return tax_by_rate

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

            lines = []
            for line in inv.invoice_line:
                line_dic = {'price_unit': line.price_unit, 'discount': line.discount, 'quantity': line.quantity,
                    'taxes': [], 'product': line.product_id}
                for tax in line.invoice_line_tax_id:
                    line_dic['taxes'].append(tax)
                lines.append(line_dic)

            tax_by_rate = self.compute_taxes_by_rate(cr, uid, lines=lines, precision=precision,
                address_id=inv.address_invoice_id.id, partner=inv.partner_id)

            # compute the tax amount of tax_grouped (old wrong amount), grouped by tax rate
            wrong_tax_by_rate = {}
            for inv_tax in tax_grouped.values():
                if not wrong_tax_by_rate.get(inv_tax['tax_id'], False):
                    wrong_tax_by_rate[inv_tax['tax_id']] = 0
                wrong_tax_by_rate[inv_tax['tax_id']] += inv_tax['tax_amount']

            # compute the difference between correct and wrong amount
            difference_by_rate = {}
            for tax_id in tax_by_rate:
                difference_by_rate[tax_id] = tax_by_rate[tax_id] - wrong_tax_by_rate[tax_id]

            for tax_id in difference_by_rate:
                tax = tax_obj.browse(cr, uid, tax_id)
                value_set = False
                # first try to add difference to non deductible tax
                for inv_tax in tax_grouped.values():
                    if inv_tax['tax_rate'] == tax.amount:
                        if inv_tax['base_code_id'] == False:
                            inv_tax['tax_amount'] =  inv_tax['tax_amount'] + difference_by_rate[tax_id]
                            inv_tax['amount'] =  inv_tax['amount'] + difference_by_rate[tax_id]
                            value_set = True
                            break
                # else add it to the normal tax
                if not value_set:
                    for inv_tax in tax_grouped.values():
                        if inv_tax['tax_rate'] == tax.amount:
                            inv_tax['tax_amount'] =  inv_tax['tax_amount'] + difference_by_rate[tax_id]
                            inv_tax['amount'] =  inv_tax['amount'] + difference_by_rate[tax_id]
                            value_set = True
                            break

        return tax_grouped
    
account_invoice_tax()    

