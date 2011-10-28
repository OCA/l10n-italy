# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#    All Rights Reserved 
#    Thanks to Cecchi s.r.l http://www.cecchi.com/
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
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

from operator import itemgetter
from osv import fields, osv
from tools.translate import _

class account_move_line(osv.osv):
    _inherit = "account.move.line"

    def amount_to_pay(self, cr, uid, ids, name, arg={}, context=None):
        """ Return the amount still to pay regarding all the riba orders
        (excepting cancelled orders)"""
        if not ids:
            return {}
        cr.execute("""SELECT ml.id,
                    CASE WHEN ml.amount_currency < 0
                        THEN - ml.amount_currency
                        ELSE ml.debit
                    END -
                    (SELECT coalesce(sum(amount_currency),0)
                        FROM riba_line rl
                            INNER JOIN riba_order ro
                                ON (rl.order_id = ro.id)
                        WHERE move_line_id = ml.id
                        AND ro.state != 'cancel') AS amount
                    FROM account_move_line ml
                    WHERE id IN %s""", (tuple(ids),))
        r = dict(cr.fetchall())
        return r
    

    def _to_pay_search(self, cr, uid, obj, name, args, context=None):
        if not args:
            return []
        line_obj = self.pool.get('account.move.line')
        query = line_obj._query_get(cr, uid, context={})
        where = ' and '.join(map(lambda x: '''(SELECT
        CASE WHEN l.amount_currency < 0
            THEN - l.amount_currency
            ELSE l.debit
        END - coalesce(sum(rl.amount_currency), 0)
        FROM riba_line rl
        INNER JOIN riba_order ro ON (rl.order_id = ro.id)
        WHERE move_line_id = l.id
        AND ro.state != 'cancel'
        ) %(operator)s %%s ''' % {'operator': x[1]}, args))
        sql_args = tuple(map(itemgetter(2), args))

        cr.execute(('''SELECT id
            FROM account_move_line l
            WHERE account_id IN (select id
                FROM account_account
                WHERE type=%s AND active)
            AND reconcile_id IS NOT NULL
            AND debit > 0
            AND ''' + where + ' and ' + query), ('receivable',)+sql_args )
        res = cr.fetchall()
        if not res:
            return [('id', '=', '0')]
        return [('id', 'in', map(lambda x:x[0], res))]

    def line2bank(self, cr, uid, ids, payment_type=None, context=None):
        """
        Try to return for each Ledger Posting line a corresponding bank
        account according to the payment type.  This work using one of
        the bank of the partner defined on the invoice eventually
        associated to the line.
        Return the last suitable bank for the corresponding partner.
        """
        riba_line_obj = self.pool.get('riba.line')
        line2bank = {}
        if not ids:
            return {}
        bank_type = riba_line_obj.s_bank_types(cr, uid, payment_type,
                context=context)
        for line in self.browse(cr, uid, ids, context=context):
            line2bank[line.id] = False
            if line.invoice and line.invoice.partner_bank_id:
                line2bank[line.id] = line.invoice.partner_bank_id.id
            elif line.partner_id:
                if not line.partner_id.bank_ids:
                    line2bank[line.id] = False
                else:
                    for bank in line.partner_id.bank_ids:
                        if bank.state in bank_type:
                            line2bank[line.id] = bank.id
                            break
                if not line2bank[line.id] and line.partner_id.bank_ids:
                    line2bank[line.id] = line.partner_id.bank_ids[-1].id
            else:
                raise osv.except_osv(_('Error !'), _('No partner defined on entry line'))
        return line2bank

    def line2iban(self, cr, uid, ids, payment_type=None, context=None):
        """
        Try to return for each Ledger Posting line a corresponding code
        iban to the payment type.  This work using one of
        the bank of the partner defined on the invoice eventually
        associated to the line.
        Return the last suitable bank for the corresponding partner.
        """
        riba_line_obj = self.pool.get('riba.line')
        line2iban = {}
        if not ids:
            return {}
        bank_type = riba_line_obj.s_bank_types(cr, uid, payment_type,
                context=context)
        for line in self.browse(cr, uid, ids, context=context):
            line2iban[line.id] = False
            if line.invoice and line.invoice.partner_bank_id:
                line2iban[line.id] = line.invoice.partner_bank_id.id.iban
            elif line.partner_id:
                if not line.partner_id.bank_ids:
                    line2iban[line.id] = False
                else:
                    for bank in line.partner_id.bank_ids:
                        if bank.state in bank_type:
                            line2iban[line.id] = bank.id.iban
                            break
                if not line2iban[line.id] and line.partner_id.bank_ids:
                    line2iban[line.id] = line.partner_id.bank_ids[-1].iban
            else:
                raise osv.except_osv(_('Error !'), _('No partner defined on entry line'))
        return line2iban

    _columns = {
        'amount_to_pay': fields.function(amount_to_pay, method=True,
            type='float', string='Amount to pay', fnct_search=_to_pay_search),
    }

account_move_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
