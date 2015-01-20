# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-2012 Domsense s.r.l. (<http://www.domsense.com>).
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2013 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
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

from openerp.osv import orm, fields
from openerp.tools.translate import _
import math
import openerp.addons.decimal_precision as dp
from datetime import datetime
from dateutil.relativedelta import relativedelta


class account_vat_period_end_statement(orm.Model):

    def _compute_authority_vat_amount(self, cr, uid, ids, field_name, arg,
                                      context):
        res = {}
        for i in ids:
            statement = self.browse(cr, uid, i)
            debit_vat_amount = 0.0
            credit_vat_amount = 0.0
            generic_vat_amount = 0.0
            for debit_line in statement.debit_vat_account_line_ids:
                debit_vat_amount += debit_line.amount
            for credit_line in statement.credit_vat_account_line_ids:
                credit_vat_amount += credit_line.amount
            for generic_line in statement.generic_vat_account_line_ids:
                generic_vat_amount += generic_line.amount
            # check if company has quarterly vat
            company = self.pool['res.users'].browse(
                cr, uid, uid, context).company_id
            authority_amount = (
                debit_vat_amount - credit_vat_amount - generic_vat_amount -
                statement.previous_credit_vat_amount +
                statement.previous_debit_vat_amount) * (
                    company.quarterly_vat and (
                        (100 + company.amount_interest) / 100.00) or 1.0)
            res[i] = authority_amount
        return res

    def _compute_payable_vat_amount(self, cr, uid, ids, field_name, arg,
                                    context):
        res = {}
        for i in ids:
            statement = self.browse(cr, uid, i)
            debit_vat_amount = 0.0
            for debit_line in statement.debit_vat_account_line_ids:
                debit_vat_amount += debit_line.amount
            res[i] = debit_vat_amount
        return res

    def _compute_deductible_vat_amount(self, cr, uid, ids, field_name, arg,
                                       context):
        res = {}
        for i in ids:
            statement = self.browse(cr, uid, i)
            credit_vat_amount = 0.0
            for credit_line in statement.credit_vat_account_line_ids:
                credit_vat_amount += credit_line.amount
            res[i] = credit_vat_amount
        return res

    # Workflow stuff
    #################

    def _reconciled(self, cr, uid, ids, name, args, context=None):
        res = {}
        for id in ids:
            res[id] = self.test_paid(cr, uid, [id])
        return res

    def move_line_id_payment_gets(self, cr, uid, ids, *args):
        res = {}
        if not ids: return res
        cr.execute('SELECT statement.id, l.id '\
                   'FROM account_move_line l '\
                   'LEFT JOIN account_vat_period_end_statement statement ON (statement.move_id=l.move_id) '\
                   'WHERE statement.id IN %s '\
                   'AND l.account_id=statement.authority_vat_account_id',
                   (tuple(ids),))
        for r in cr.fetchall():
            res.setdefault(r[0], [])
            res[r[0]].append( r[1] )
        return res

    # return the ids of the move lines which has the same account than the statement
    # whose id is in ids
    def move_line_id_payment_get(self, cr, uid, ids, *args):
        if not ids: return []
        result = self.move_line_id_payment_gets(cr, uid, ids, *args)
        return result.get(ids[0], [])

    def test_paid(self, cr, uid, ids, *args):
        res = self.move_line_id_payment_get(cr, uid, ids)
        if not res:
            return False
        ok = True
        for id in res:
            cr.execute('select reconcile_id from account_move_line where id=%s', (id,))
            ok = ok and  bool(cr.fetchone()[0])
        return ok

    def _get_statement_from_line(self, cr, uid, ids, context=None):
        move = {}
        for line in self.pool.get('account.move.line').browse(cr, uid, ids, context=context):
            if line.reconcile_partial_id:
                for line2 in line.reconcile_partial_id.line_partial_ids:
                    move[line2.move_id.id] = True
            if line.reconcile_id:
                for line2 in line.reconcile_id.line_id:
                    move[line2.move_id.id] = True
        statement_ids = []
        if move:
            statement_ids = self.pool.get('account.vat.period.end.statement').search(
                cr, uid, [('move_id','in',move.keys())], context=context)
        return statement_ids

    def _get_statement_from_move(self, cr, uid, ids, context=None):
        move = {}
        statement_ids = []
        for move in self.pool.get('account.move').browse(cr, uid, ids, context=context):
            found_ids = self.pool.get('account.vat.period.end.statement').search(
                cr, uid, [('move_id','=',move.id)], context=context)
            for found_id in found_ids:
                if found_id not in statement_ids:
                    statement_ids.append(found_id)
        return statement_ids

    def _get_statement_from_reconcile(self, cr, uid, ids, context=None):
        move = {}
        for r in self.pool.get('account.move.reconcile').browse(cr, uid, ids, context=context):
            for line in r.line_partial_ids:
                move[line.move_id.id] = True
            for line in r.line_id:
                move[line.move_id.id] = True

        statement_ids = []
        if move:
            statement_ids = self.pool.get('account.vat.period.end.statement').search(
                cr, uid, [('move_id','in',move.keys())], context=context)
        return statement_ids

    def _get_credit_line(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('statement.credit.account.line').browse(cr, uid, ids, context=context):
            result[line.statement_id.id] = True
        return result.keys()

    def _get_debit_line(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('statement.debit.account.line').browse(cr, uid, ids, context=context):
            result[line.statement_id.id] = True
        return result.keys()

    def _get_generic_line(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('statement.generic.account.line').browse(cr, uid, ids, context=context):
            result[line.statement_id.id] = True
        return result.keys()

    def _amount_residual(self, cr, uid, ids, name, args, context=None):
        result = {}
        for statement in self.browse(cr, uid, ids, context=context):
            result[statement.id] = 0.0
            if statement.move_id:
                for m in statement.move_id.line_id:
                    if m.account_id.type in ('receivable','payable'):
                        result[statement.id] += m.amount_residual_currency
        return result

    def _compute_lines(self, cr, uid, ids, name, args, context=None):
        result = {}
        for statement in self.browse(cr, uid, ids, context=context):
            src = []
            lines = []
            if statement.move_id:
                for m in statement.move_id.line_id:
                    temp_lines = []
                    if m.reconcile_id:
                        temp_lines = map(lambda x: x.id, m.reconcile_id.line_id)
                    elif m.reconcile_partial_id:
                        temp_lines = map(lambda x: x.id, m.reconcile_partial_id.line_partial_ids)
                    lines += [x for x in temp_lines if x not in lines]
                    src.append(m.id)

            lines = filter(lambda x: x not in src, lines)
            result[statement.id] = lines
        return result

    _name = "account.vat.period.end.statement"
    _rec_name = 'date'
    _columns = {
        'debit_vat_account_line_ids': fields.one2many('statement.debit.account.line', 'statement_id', 'Debit VAT', help='The accounts containing the debit VAT amount to write-off', states={'confirmed': [('readonly', True)], 'paid': [('readonly', True)], 'draft': [('readonly', False)]}),

        'credit_vat_account_line_ids': fields.one2many('statement.credit.account.line', 'statement_id', 'Credit VAT', help='The accounts containing the credit VAT amount to write-off', states={'confirmed': [('readonly', True)], 'paid': [('readonly', True)], 'draft': [('readonly', False)]}),

        'previous_credit_vat_account_id': fields.many2one('account.account', 'Previous Credits VAT', help='Credit VAT from previous periods', states={'confirmed': [('readonly', True)], 'paid': [('readonly', True)], 'draft': [('readonly', False)]}),
        'previous_credit_vat_amount': fields.float('Previous Credits VAT Amount', states={'confirmed': [('readonly', True)], 'paid': [('readonly', True)], 'draft': [('readonly', False)]},
            digits_compute=dp.get_precision('Account')),

        'previous_debit_vat_account_id': fields.many2one('account.account', 'Previous Debits VAT', help='Debit VAT from previous periods', states={'confirmed': [('readonly', True)], 'paid': [('readonly', True)], 'draft': [('readonly', False)]}),
        'previous_debit_vat_amount': fields.float('Previous Debits VAT Amount', states={'confirmed': [('readonly', True)], 'paid': [('readonly', True)], 'draft': [('readonly', False)]},
            digits_compute=dp.get_precision('Account')),

        'generic_vat_account_line_ids': fields.one2many('statement.generic.account.line', 'statement_id', 'Other VAT Credits / Debits or Tax Compensations', states={'confirmed': [('readonly', True)], 'paid': [('readonly', True)], 'draft': [('readonly', False)]}),

        'authority_partner_id': fields.many2one('res.partner', 'Tax Authority Partner', states={'confirmed': [('readonly', True)], 'paid': [('readonly', True)], 'draft': [('readonly', False)]}),
        'authority_vat_account_id': fields.many2one('account.account', 'Tax Authority VAT Account', required=True, states={'confirmed': [('readonly', True)], 'paid': [('readonly', True)], 'draft': [('readonly', False)]}),
        'authority_vat_amount': fields.function(
            _compute_authority_vat_amount, method=True,
            string='Authority VAT Amount'),
        'payable_vat_amount': fields.function(_compute_payable_vat_amount, method=True, string='Payable VAT Amount'),
        'deductible_vat_amount': fields.function(_compute_deductible_vat_amount, method=True, string='Deductible VAT Amount'),

        'journal_id': fields.many2one('account.journal', 'Journal', required=True, states={'confirmed': [('readonly', True)], 'paid': [('readonly', True)], 'draft': [('readonly', False)]}),
        'date': fields.date('Date', required=True, states={'confirmed': [('readonly', True)], 'paid': [('readonly', True)], 'draft': [('readonly', False)]}),
        'move_id': fields.many2one('account.move', 'VAT statement move', readonly=True),
        #'voucher_id': fields.many2one('account.voucher', 'VAT payment', readonly=True),

        'state': fields.selection([
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('paid', 'Paid'),
            ], 'State', readonly=True),
            
        'payment_term_id': fields.many2one('account.payment.term', 'Payment Term',
            states={'confirmed': [('readonly', True)], 'paid': [('readonly', True)],
            'draft': [('readonly', False)]}),

        'reconciled': fields.function(_reconciled, string='Paid/Reconciled', type='boolean',
            store={
                'account.vat.period.end.statement': (lambda self, cr, uid, ids, c={}: ids, None, 50),
                'account.move.line': (_get_statement_from_line, None, 50),
                'account.move.reconcile': (_get_statement_from_reconcile, None, 50),
            }, help="It indicates that the statement has been paid and the journal entry of the statement has been reconciled with one or several journal entries of payment."),
        'residual': fields.function(_amount_residual, digits_compute=dp.get_precision('Account'), string='Balance',
            store={
                'account.vat.period.end.statement': (lambda self, cr, uid, ids, c={}: ids,
                    ['debit_vat_account_line_ids', 'credit_vat_account_line_ids',
                    'generic_vat_account_line_ids', 'move_id', 'state'], 50),
                'statement.credit.account.line': (_get_credit_line, ['amount','statement_id'], 50),
                'statement.debit.account.line': (_get_debit_line, ['amount','statement_id'], 50),
                'statement.generic.account.line': (_get_generic_line, ['amount','statement_id'], 50),
                'account.move': (_get_statement_from_move, None, 50),
                'account.move.line': (_get_statement_from_line, None, 50),
                'account.move.reconcile': (_get_statement_from_reconcile, None, 50),
            },
            help="Remaining amount due."),
        'payment_ids': fields.function(_compute_lines, relation='account.move.line', type="many2many", string='Payments'),
        'period_ids': fields.one2many('account.period','vat_statement_id','Periods'),
    }

    _defaults = {
        'date': fields.date.context_today,
    }

    def _get_tax_code_amount(self, cr, uid, tax_code_id, period_id, context):
        if not context:
            context={}
        context['period_id'] = period_id
        return self.pool.get('account.tax.code').browse(cr, uid, tax_code_id, context)._sum_period(
            None, None, context)[tax_code_id]

    def unlink(self, cr, uid, ids, context=None):
        if isinstance(ids, (long,int)):
            ids = [ids]
        for statement in self.browse(cr, uid, ids, context):
            if statement.state == 'confirmed' or statement.state == 'paid':
                raise orm.except_orm(_('Error!'), _('You cannot delete a confirmed or paid statement'))
        res = super(account_vat_period_end_statement, self).unlink(cr, uid, ids, context)
        return res

    def statement_draft(self, cr, uid, ids, context=None):
        for statement in self.browse(cr, uid, ids, context):
            if statement.move_id:
                statement.move_id.unlink()
            '''
            if statement.voucher_id:
                statement.voucher_id.unlink()
            '''
        self.write(cr, uid, ids , {'state': 'draft'})

    def statement_paid(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids , {'state': 'paid'})

    def create_move(self, cr, uid, ids, context=None):
        move_obj = self.pool.get('account.move')
        term_pool = self.pool.get('account.payment.term')
        line_obj = self.pool.get('account.move.line')
        period_obj = self.pool.get('account.period')
        for statement in self.browse(cr, uid, ids, context):
            period_ids = period_obj.find(
                cr, uid, dt=statement.date, context=context)
            # check if company has quarterly vat
            quarterly_vat = self.pool['res.users'].browse(
                cr, uid, uid, context).company_id.quarterly_vat
            if (quarterly_vat and len(statement.period_ids) != 3):
                raise orm.except_orm(
                    _('Encoding error'),
                    _("No quarterly found or more than three periods found"
                      " for the given date."))
            elif len(period_ids) != 1:
                raise orm.except_orm(
                    _('Encoding error'),
                    _("No period found or more than one period found for "
                      "the given date."))
            move_data = {
                'name': _('VAT statement') + ' - ' + statement.date,
                'date': statement.date,
                'journal_id': statement.journal_id.id,
                'period_id': period_ids[0],
                }
            move_id = move_obj.create(cr, uid, move_data)
            statement.write({'move_id': move_id})

            for debit_line in statement.debit_vat_account_line_ids:
                debit_vat_data = {
                    'name': _('Debit VAT'),
                    'account_id': debit_line.account_id.id,
                    'move_id': move_id,
                    'journal_id': statement.journal_id.id,
                    'debit': 0.0,
                    'credit': 0.0,
                    'date': statement.date,
                    'period_id': period_ids[0],
                    }
                if debit_line.amount > 0:
                    debit_vat_data['debit'] = math.fabs(debit_line.amount)
                else:
                    debit_vat_data['credit'] = math.fabs(debit_line.amount)
                line_obj.create(cr, uid, debit_vat_data)

            for credit_line in statement.credit_vat_account_line_ids:
                credit_vat_data = {
                    'name': _('Credit VAT'),
                    'account_id': credit_line.account_id.id,
                    'move_id': move_id,
                    'journal_id': statement.journal_id.id,
                    'debit': 0.0,
                    'credit': 0.0,
                    'date': statement.date,
                    'period_id': period_ids[0],
                    }
                if credit_line.amount < 0:
                    credit_vat_data['debit'] = math.fabs(credit_line.amount)
                else:
                    credit_vat_data['credit'] = math.fabs(credit_line.amount)
                line_obj.create(cr, uid, credit_vat_data)

            if statement.previous_credit_vat_amount:
                previous_credit_vat_data = {
                    'name': _('Previous Credits VAT'),
                    'account_id': statement.previous_credit_vat_account_id.id,
                    'move_id': move_id,
                    'journal_id': statement.journal_id.id,
                    'debit': 0.0,
                    'credit': 0.0,
                    'date': statement.date,
                    'period_id': period_ids[0],
                    }
                if statement.previous_credit_vat_amount < 0:
                    previous_credit_vat_data['debit'] = math.fabs(statement.previous_credit_vat_amount)
                else:
                    previous_credit_vat_data['credit'] = math.fabs(statement.previous_credit_vat_amount)
                line_obj.create(cr, uid, previous_credit_vat_data)

            if statement.previous_debit_vat_amount:
                previous_debit_vat_data = {
                    'name': _('Previous Debits VAT'),
                    'account_id': statement.previous_debit_vat_account_id.id,
                    'move_id': move_id,
                    'journal_id': statement.journal_id.id,
                    'debit': 0.0,
                    'credit': 0.0,
                    'date': statement.date,
                    'period_id': period_ids[0],
                    }
                if statement.previous_debit_vat_amount > 0:
                    previous_debit_vat_data['debit'] = math.fabs(statement.previous_debit_vat_amount)
                else:
                    previous_debit_vat_data['credit'] = math.fabs(statement.previous_debit_vat_amount)
                line_obj.create(cr, uid, previous_debit_vat_data)

            for generic_line in statement.generic_vat_account_line_ids:
                generic_vat_data = {
                    'name': _('Other VAT Credits / Debits'),
                    'account_id': generic_line.account_id.id,
                    'move_id': move_id,
                    'journal_id': statement.journal_id.id,
                    'debit': 0.0,
                    'credit': 0.0,
                    'date': statement.date,
                    'period_id': period_ids[0],
                    }
                if generic_line.amount < 0:
                    generic_vat_data['debit'] = math.fabs(generic_line.amount)
                else:
                    generic_vat_data['credit'] = math.fabs(generic_line.amount)
                line_obj.create(cr, uid, generic_vat_data)

            end_debit_vat_data = {
                'name': _('Tax Authority VAT'),
                'account_id': statement.authority_vat_account_id.id,
                'partner_id': statement.authority_partner_id.id,
                'move_id': move_id,
                'journal_id': statement.journal_id.id,
                'date': statement.date,
                'period_id': period_ids[0],
                }
            if statement.authority_vat_amount > 0:
                end_debit_vat_data['debit'] = 0.0
                end_debit_vat_data['credit'] = math.fabs(statement.authority_vat_amount)
                if statement.payment_term_id:
                    due_list = term_pool.compute(
                        cr, uid, statement.payment_term_id.id, math.fabs(statement.authority_vat_amount),
                        date_ref=statement.date, context=context)
                    if len(due_list) == 0:
                        raise orm.except_orm(_('Error'),
                            _('The payment term %s does not have due dates')
                            % statement.payment_term_id.name)
                    for term in due_list:
                        current_line = end_debit_vat_data
                        current_line['credit'] = term[1]
                        current_line['date_maturity'] = term[0]
                        line_obj.create(cr, uid, current_line)
                else:
                    line_obj.create(cr, uid, end_debit_vat_data)
            elif statement.authority_vat_amount < 0:
                end_debit_vat_data['debit'] = math.fabs(statement.authority_vat_amount)
                end_debit_vat_data['credit'] = 0.0
                line_obj.create(cr, uid, end_debit_vat_data)

            self.write(cr, uid, statement.id , {'state': 'confirmed'})

        return True

    """
    def open_chart_of_taxes(self, cr, uid, ids, context=None):
        result = {}
        if context is None:
            context = {}
        for statement in self.browse(cr, uid, ids, context):
            mod_obj = self.pool.get('ir.model.data')
            act_obj = self.pool.get('ir.actions.act_window')
            period_obj = self.pool.get('account.period')
            period_ids = period_obj.find(cr, uid, dt=statement.date, context=context)
            if len(period_ids)> 1:
                raise orm.except_orm(_('Error'), _('Too many periods for date %s') % str(statement.date))
            period = period_obj.browse(cr, uid, period_ids[0], context)
            result = mod_obj.get_object_reference(cr, uid, 'account', 'action_tax_code_tree')
            id = result and result[1] or False
            result = act_obj.read(cr, uid, [id], context=context)[0]

            fiscalyear_id = period.fiscalyear_id.id
            result['context'] = str({'period_id': period.id, \
                                     'fiscalyear_id': fiscalyear_id, \
                                        'state': 'posted'})

            period_code = period.code
            result['name'] += period_code and (':' + period_code) or ''
            result['nodestroy'] = True
        return result
    """
    
    def compute_amounts(self, cr, uid, ids, context=None):
        debit_line_pool=self.pool.get('statement.debit.account.line')
        credit_line_pool=self.pool.get('statement.credit.account.line')
        for statement in self.browse(cr, uid, ids, context):
            statement.write({'previous_debit_vat_amount': 0.0})
            prev_statement_ids = self.search(cr, uid, [('date', '<', statement.date)], order='date')
            if prev_statement_ids:
                prev_statement = self.browse(cr, uid,
                    prev_statement_ids[len(prev_statement_ids)-1], context)
                if (prev_statement.residual > 0 and
                        prev_statement.authority_vat_amount > 0):
                    statement.write({
                        'previous_debit_vat_amount': prev_statement.residual})
                elif prev_statement.authority_vat_amount < 0:
                    statement.write({
                        'previous_credit_vat_amount': - prev_statement.authority_vat_amount})

            credit_line_ids = []
            debit_line_ids = []
            tax_code_pool = self.pool.get('account.tax.code')
            debit_tax_code_ids = tax_code_pool.search(cr, uid, [
                ('vat_statement_account_id', '!=', False),
                ('vat_statement_type', '=', 'debit'),
                ], context=context)
            for debit_tax_code_id in debit_tax_code_ids:
                debit_tax_code = tax_code_pool.browse(
                    cr, uid, debit_tax_code_id, context)
                total = 0.0
                for period in statement.period_ids:
                    context['period_id'] = period.id
                    total += tax_code_pool.browse(
                        cr, uid, debit_tax_code_id, context).sum_period
                debit_line_ids.append({
                    'account_id': debit_tax_code.vat_statement_account_id.id,
                    'tax_code_id': debit_tax_code.id,
                    'amount': (total * debit_tax_code.vat_statement_sign),
                    })

            credit_tax_code_ids = tax_code_pool.search(cr, uid, [
                ('vat_statement_account_id', '!=', False),
                ('vat_statement_type', '=', 'credit'),
                ], context=context)
            for credit_tax_code_id in credit_tax_code_ids:
                credit_tax_code = tax_code_pool.browse(
                    cr, uid, credit_tax_code_id, context)
                total = 0.0
                for period in statement.period_ids:
                    context['period_id'] = period.id
                    total += tax_code_pool.browse(
                        cr, uid, credit_tax_code_id, context).sum_period
                credit_line_ids.append({
                    'account_id': credit_tax_code.vat_statement_account_id.id,
                    'tax_code_id': credit_tax_code.id,
                    'amount': total * credit_tax_code.vat_statement_sign,
                    })
            
            for debit_line in statement.debit_vat_account_line_ids:
                debit_line.unlink()
            for credit_line in statement.credit_vat_account_line_ids:
                credit_line.unlink()
            for debit_vals in debit_line_ids:
                debit_vals.update({'statement_id': statement.id})
                debit_line_pool.create(cr, uid, debit_vals, context=context)
            for credit_vals in credit_line_ids:
                credit_vals.update({'statement_id': statement.id})
                credit_line_pool.create(cr, uid, credit_vals, context=context)
        return True

    def on_change_partner_id(self, cr, uid, ids, partner_id, context=None):
        partner = self.pool.get('res.partner').browse(cr, uid, partner_id, context)
        return {'value': {'authority_vat_account_id': partner.property_account_payable.id}}

class statement_debit_account_line(orm.Model):
    _name='statement.debit.account.line'
    _columns = {
        'account_id': fields.many2one('account.account', 'Account', required=True),
        'tax_code_id': fields.many2one('account.tax.code', 'Tax Code', required=True),
        'statement_id': fields.many2one('account.vat.period.end.statement', 'VAT statement'),
        'amount': fields.float('Amount', digits_compute= dp.get_precision('Account'), required=True),
        }

class statement_credit_account_line(orm.Model):
    _name='statement.credit.account.line'
    _columns = {
        'account_id': fields.many2one('account.account', 'Account', required=True),
        'tax_code_id': fields.many2one('account.tax.code', 'Tax Code', required=True),
        'statement_id': fields.many2one('account.vat.period.end.statement', 'VAT statement'),
        'amount': fields.float('Amount', digits_compute= dp.get_precision('Account'), required=True),
        }

class statement_generic_account_line(orm.Model):
    _name='statement.generic.account.line'
    _columns = {
        'account_id': fields.many2one('account.account', 'Account', required=True),
        'statement_id': fields.many2one('account.vat.period.end.statement', 'VAT statement'),
        'amount': fields.float('Amount', digits_compute= dp.get_precision('Account'), required=True),
        }

    def on_change_vat_account_id(self, cr, uid, ids, vat_account_id=False, context=None):
        res = {}
        res['value'] = {}
        if not vat_account_id:
            return res
        res['value']['amount'] = self.pool.get('account.account').browse(cr, uid, vat_account_id,
            context).balance
        return res

class account_tax_code(orm.Model):
    _inherit = "account.tax.code"
    _columns = {
        'vat_statement_account_id': fields.many2one('account.account', "Account used for VAT statement. The tax code balance will be associated to this account after selecting the period in VAT statement"),
        'vat_statement_type': fields.selection([('credit','Credit'),('debit','Debit')], 'Type', help="This establish whether amount will be loaded as debit or credit"),
        'vat_statement_sign': fields.integer('Sign used in statement', help="If tax code period sum is usually negative, set '-1' here"),
        }
    _defaults = {
        'vat_statement_type': 'debit',
        'vat_statement_sign': 1,
    }

class account_period(orm.Model):
    _inherit = "account.period"
    _columns = {
        'vat_statement_id': fields.many2one('account.vat.period.end.statement', "VAT statement"),
        }
