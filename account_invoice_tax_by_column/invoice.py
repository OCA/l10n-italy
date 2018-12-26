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
from tools.translate import _

class account_invoice(osv.osv):

    _inherit = 'account.invoice'
    
    _columns = {
        'vertical_comp' : fields.boolean('Tax Computation By Column'),
    }
    
    _defaults = {
        'vertical_comp': True
    }

account_invoice()

class account_invoice_tax(osv.osv):

    _inherit = "account.invoice.tax"

    def compute(self, cr, uid, invoice_id, context=None):
        tax_grouped = super(account_invoice_tax, self).compute(cr, uid, invoice_id, context)
        inv_obj = self.pool.get('account.invoice')
        tax_obj = self.pool.get('account.tax')
        tax_code_obj = self.pool.get('account.tax.code')
        inv = inv_obj.browse(cr, uid, invoice_id, context=context)
        if inv.vertical_comp:
            cur = inv.currency_id
            company_currency = inv.company_id.currency_id.id
            tax_obj = self.pool.get('account.tax')
            user_obj = self.pool.get('res.users')
            cur_obj = self.pool.get('res.currency')
            precision = self.pool.get('decimal.precision').precision_get(cr, uid, 'Account')

            for inv_tax in tax_grouped.values():
                if inv_tax['tax_code_id']:
                    main_tax = tax_obj.get_main_tax(tax_obj.get_account_tax_by_tax_code(
                        tax_code_obj.browse(cr, uid, inv_tax['tax_code_id'])))
                elif inv_tax['base_code_id']:
                    main_tax = tax_obj.get_main_tax(tax_obj.get_account_tax_by_base_code(
                        tax_code_obj.browse(cr, uid, inv_tax['base_code_id'])))
                else:
                    raise osv.except_osv(_('Error'),
                        _('No tax codes for invoice tax %s') % inv_tax['name'])
                if main_tax.price_include:
                    continue
                if inv_tax['amount'] and inv_tax['base']:
                    inv_tax['amount'] = cur_obj.round(cr, uid, cur, inv_tax['base'] * main_tax.amount)
                    if inv.type in ('out_invoice','in_invoice'):
                        inv_tax['tax_amount'] = cur_obj.compute(cr, uid, inv.currency_id.id, company_currency,
                            inv_tax['amount'] * main_tax['tax_sign'],
                            context={'date': inv.date_invoice or time.strftime('%Y-%m-%d')}, round=False)
                    else:
                        inv_tax['tax_amount'] = cur_obj.compute(cr, uid, inv.currency_id.id, company_currency,
                            inv_tax['amount'] * main_tax['ref_tax_sign'],
                            context={'date': inv.date_invoice or time.strftime('%Y-%m-%d')}, round=False)
                    inv_tax['tax_amount'] = cur_obj.round(cr, uid, cur, inv_tax['tax_amount'])

        return tax_grouped
    
account_invoice_tax()    

