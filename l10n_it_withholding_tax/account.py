# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2012 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>). 
#    All Rights Reserved
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
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

from osv import fields, osv
from tools.translate import _

class account_tax(osv.osv):
    _inherit = 'account.tax'
    _columns = {
        'withholding_tax': fields.boolean('Withholding Tax'),
        'withholding_payment_term_id': fields.many2one('account.payment.term', 'Withholding Payment Term'),
        }
account_tax()

class account_invoice(osv.osv):
    _inherit = "account.invoice"
    
    def action_move_create(self, cr, uid, ids, context=None):
        res = super(account_invoice, self).action_move_create(cr, uid, ids, context=context)
        tax_pool = self.pool.get('account.tax')
        term_pool = self.pool.get('account.payment.term')
        for inv in self.browse(cr, uid, ids, context=context):
            for move_line in inv.move_id.line_id:
                if move_line.tax_code_id:
                    tax_ids = tax_pool.search(cr, uid, [('tax_code_id', '=', move_line.tax_code_id.id)])
                    is_withholding = False
                    for tax in tax_pool.browse(cr, uid, tax_ids):
                        if tax.withholding_tax:
                            is_withholding = True
                    if is_withholding:
                        if len(tax_ids) > 1:
                            raise osv.except_osv(_('Error'),
                                _('Too many taxes associated to tax.code %s') % move_line.tax_code_id.name)
                        if not tax_ids:
                            raise osv.except_osv(_('Error'),
                                _('No taxes associated to tax.code %s') % move_line.tax_code_id.name)
                        tax = tax_pool.browse(cr, uid, tax_ids[0])
                        if tax.withholding_tax and tax.withholding_payment_term_id:
                            due_list = term_pool.compute(
                                cr, uid, tax.withholding_payment_term_id.id, move_line.tax_amount,
                                date_ref=inv.date_invoice, context=context)
                            if len(due_list) > 1:
                                raise osv.except_osv(_('Error'),
                                    _('The payment term %s has too many due dates')
                                    % tax.withholding_payment_term_id.name)
                            if len(due_list) == 0:
                                raise osv.except_osv(_('Error'),
                                    _('The payment term %s does not have due dates')
                                    % tax.withholding_payment_term_id.name)
                            move_line.write({'date_maturity': due_list[0][0]})
        return res

account_invoice()
