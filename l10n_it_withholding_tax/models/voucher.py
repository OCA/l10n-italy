# -*- coding: utf-8 -*-
# Copyright © 2015 Alessandro Camilli (<http://www.openforce.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import orm, fields
import openerp.addons.decimal_precision as dp


class AccountVoucher(orm.Model):
    _inherit = "account.voucher"

    def recompute_voucher_lines(self, cr, uid, ids, partner_id, journal_id,
                                price, currency_id, ttype, date, context=None):
        """
        Compute original amount of WT of rate
        """
        move_line_obj = self.pool['account.move.line']
        voucher_line_obj = self.pool['account.voucher.line']
        dp_obj = self.pool['decimal.precision']
        res = super(AccountVoucher, self).recompute_voucher_lines(
            cr, uid, ids, partner_id, journal_id, price, currency_id, ttype,
            date, context=context)

        def _compute_wt_values(lines):
            amount_overflow_residual = 0.0
            # For each line, WT
            for line in lines:
                if 'move_line_id' in line and line['move_line_id']:
                    move_line = move_line_obj.browse(cr, uid,
                                                     line['move_line_id'])
                    line['amount_original_withholding_tax'] = \
                        move_line.withholding_tax_amount
                    line['amount_residual_withholding_tax'] = \
                        voucher_line_obj.\
                        compute_amount_residual_withholdin_tax(
                        cr, uid, line, context=None)
            # Recompute automatic values on amount:
            # The amount_residual_currency on account_move_line, doesn't see
            # the WT values
            if lines and lines[0]['amount']:
                # For each amount to redistribuite
                tot_amount = 0
                for line in lines:
                    tot_amount += line['amount'] + \
                        line['amount_residual_withholding_tax']

                # Redistribuite amount
                extra_amount = 0
                for line in lines:
                    if tot_amount <= 0:
                        break
                    save_amount = line['amount']
                    line['amount'] += extra_amount
                    if (
                        line['amount'] >
                        (
                            line['amount_unreconciled'] -
                            line['amount_residual_withholding_tax']
                        )
                    ):
                        line['amount'] = line['amount_unreconciled'] \
                            - line['amount_residual_withholding_tax']
                        line['amount'] = round(
                            line['amount'], dp_obj.precision_get(cr, uid,
                                                                 'Account'))
                    extra_amount += (save_amount - line['amount'])
                    tot_amount -= line['amount']
            # Allocate WT
            for line in lines:
                if 'move_line_id' in line and line['move_line_id']:
                    move_line = move_line_obj.browse(cr, uid,
                                                     line['move_line_id'])
                    if line['amount'] or amount_overflow_residual:
                        # Assign overflow from other lines
                        if amount_overflow_residual:
                            if (
                                (line['amount'] + amount_overflow_residual) <=
                                (
                                    line['amount_unreconciled'] -
                                    line['amount_residual_withholding_tax']
                                )
                            ):
                                line['amount'] += amount_overflow_residual
                                amount_overflow_residual = 0.0
                            else:
                                line['amount'] = line['amount_unreconciled'] \
                                    - line['amount_residual_withholding_tax']
                        # Compute WT
                        line['amount_withholding_tax'] = \
                            voucher_line_obj.compute_amount_withholdin_tax(
                                cr, uid, line['amount'],
                                line['amount_unreconciled'],
                                line['amount_residual_withholding_tax'],
                                context=None)
                        # WT can generate an overflow. It will bw assigned to
                        # next line
                        amount_overflow = line['amount'] \
                            + line['amount_withholding_tax'] \
                            - line['amount_unreconciled']
                        if amount_overflow > 0:
                            line['amount'] -= amount_overflow
                            amount_overflow_residual += amount_overflow
                    line['amount_original'] -= \
                        line['amount_original_withholding_tax']

            return lines
        if partner_id:
            # resolve lists of commands into lists of dicts
            line_dr_ids_ctrl = res['value']['line_dr_ids']
            line_dr_ids = []
            for l in line_dr_ids_ctrl:
                if isinstance(l, dict):
                    line_dr_ids.append(l)
            line_cr_ids_ctrl = res['value']['line_cr_ids']
            line_cr_ids = []
            for l in line_cr_ids_ctrl:
                if isinstance(l, dict):
                    line_cr_ids.append(l)

            _compute_wt_values(line_dr_ids)
            _compute_wt_values(line_cr_ids)

        return res

    def voucher_move_line_create(
            self, cr, uid, voucher_id, line_total, move_id, company_currency,
            current_currency, context=None):
        """
        Add WT line to registration and change amount on debit/credit line of
        the invoice
        """
        move_line_obj = self.pool['account.move.line']
        account_move_obj = self.pool['account.move']  # Apulia
        voucher_line_obj = self.pool['account.voucher.line']
        payment_term_obj = self.pool['account.payment.term']
        reconcile_obj = self.pool['account.move.reconcile']
        line_total, rec_list_ids = super(AccountVoucher, self).\
            voucher_move_line_create(cr, uid, voucher_id, line_total, move_id,
                                     company_currency, current_currency,
                                     context=context)

        def _unreconcile_move_line(move_line):
            """
            Remove reconciliation to change amounts
            """
            recs = []
            recs_to_rereconcile = []
            if move_line.reconcile_id:
                recs += [move_line.reconcile_id.id]
            if move_line.reconcile_partial_id:
                recs += [move_line.reconcile_partial_id.id]
                # If there are other partial payments, I save the id line to
                # future reconcile
                cr.execute('SELECT id FROM account_move_line WHERE \
                            reconcile_partial_id=%s  AND id <> %s',
                           (move_line.reconcile_partial_id.id, move_line.id))
                for l in cr.dictfetchall():
                    recs_to_rereconcile.append(l['id'])
            reconcile_obj.unlink(cr, uid, recs)
            return recs_to_rereconcile

        # rec_list_ids id payment move line with invoice move_line to reconcile
        rec_list_new_moves = []
        for rec in rec_list_ids:
            line_move_to_pay = move_line_obj.browse(cr, uid, rec[1])
            line_payment = move_line_obj.browse(cr, uid, rec[0])
            # verifica che la registrazione non sia validata e la riporta in bozza
            # Remove reconciliation to change amounts
            lines_to_rereconcile = _unreconcile_move_line(line_move_to_pay)
            for r_line_id in lines_to_rereconcile:
                rec_list_new_moves.append([r_line_id, line_move_to_pay.id])
            _unreconcile_move_line(line_payment)
            # line voucher with WT
            domain = [('voucher_id', '=', voucher_id), ('move_line_id', '=',
                                                        line_move_to_pay.id)]
            v_line_payment_ids = voucher_line_obj.search(cr, uid, domain)
            for v_line in voucher_line_obj.browse(cr, uid, v_line_payment_ids):
                voucher = v_line.voucher_id
                for wt_v_line in v_line.withholding_tax_line_ids:
                    credit = 0.0
                    debit = 0.0
                    if v_line.move_line_id.debit:
                        debit = wt_v_line.amount
                    else:
                        credit = wt_v_line.amount
                    # account
                    if line_move_to_pay.account_id.type == 'receivable':
                        wt_account_id = wt_v_line.withholding_tax_id.\
                            account_receivable_id.id
                    else:
                        wt_account_id = wt_v_line.withholding_tax_id\
                            .account_payable_id.id
                    # Line WT
                    payment_lines = payment_term_obj.compute(
                        cr, uid, wt_v_line.withholding_tax_id.payment_term.id,
                        wt_v_line.amount, voucher.date or False,
                        context=context)
                    line_wt_ids = []
                    for payment_line in payment_lines:
                        p_date_maturity = payment_line[0]
                        p_credit = 0.0
                        p_debit = 0.0
                        if debit:
                            p_debit = payment_line[1]
                        else:
                            p_credit = payment_line[1]
                        val_move_line = {
                            'journal_id': voucher.journal_id.id,
                            'period_id': voucher.period_id.id,
                            'name': (
                                wt_v_line.withholding_tax_id.name + ' ' +
                                voucher.partner_id.name or '/'),
                            'account_id': wt_account_id,
                            'move_id': move_id,
                            'partner_id': False,
                            'currency_id': (
                                v_line.move_line_id.currency_id.id or
                                False),
                            'analytic_account_id': (
                                v_line.account_analytic_id and
                                v_line.account_analytic_id.id or False),
                            'quantity': 1,
                            'credit': p_credit,
                            'debit': p_debit,
                            'date': voucher.date,
                            'date_maturity': p_date_maturity
                        }
                        line_wt_id = move_line_obj.create(cr, uid,
                                                          val_move_line)
                        line_wt_ids.append(line_wt_id)

                    # Add amount WT to line debit/credit partner
                    val = {
                        'credit': line_payment.credit + debit,
                        'debit': line_payment.debit + credit
                    }
                    # la registrazione è già validata la riporta in bozza
                    cc_move = line_payment.move_id
                    if cc_move.state == 'posted':
                        account_move_obj.button_cancel(
                            cr, uid, [cc_move.id], context)
                    move_line_obj.write(cr, uid, [line_payment.id], val)
                    # una volta corretta la riga rivalida la registrazione
                    if cc_move.journal_id.entry_posted:
                        account_move_obj.post(cr, uid, [cc_move.id], context={})

        # Merge with existing lines to reconcile
        if rec_list_new_moves:
            for rec_new in rec_list_new_moves:
                for rec_ids in rec_list_ids:
                    if not rec_new[1] == rec_ids[1]:
                        continue
                    rec_ids.append(rec_new[0])

        return (line_total, rec_list_ids)

    def action_move_line_create(self, cr, uid, ids, context=None):
        """
        Assign payment move to wt lines
        """
        res = super(AccountVoucher, self).action_move_line_create(
            cr, uid, ids, context=None)
        for voucher in self.browse(cr, uid, ids):
            for v_line in voucher.line_ids:
                for wt_v_line in v_line.withholding_tax_line_ids:
                    self.pool['withholding.tax.voucher.line']._align_wt_move(
                        cr, uid, [wt_v_line.id])
        return res


class AccountVoucherLine(orm.Model):
    _inherit = "account.voucher.line"

    def _amount_withholding_tax(self, cr, uid, ids, name, args, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = {
                'amount_original_withholding_tax': 0.0,
            }
            res[line.id]['amount_original_withholding_tax'] += \
                line.move_line_id.withholding_tax_amount
        return res

    def _compute_balance(self, cr, uid, ids, name, args, context=None):
        """
        Extends the compute of original amounts for exclude from total the WT
        amount
        """
        currency_pool = self.pool.get('res.currency')
        rs_data = {}
        for line in self.browse(cr, uid, ids, context=context):
            ctx = context.copy()
            ctx.update({'date': line.voucher_id.date})
            voucher_rate = self.pool.get('res.currency').read(
                cr, uid, line.voucher_id.currency_id.id, ['rate'],
                context=ctx)['rate']
            ctx.update({
                'voucher_special_currency':
                    line.voucher_id.payment_rate_currency_id and
                    line.voucher_id.payment_rate_currency_id.id or False,
                'voucher_special_currency_rate':
                    line.voucher_id.payment_rate * voucher_rate})
            res = {}
            company_currency = \
                line.voucher_id.journal_id.company_id.currency_id.id
            voucher_currency = line.voucher_id.currency_id \
                and line.voucher_id.currency_id.id or company_currency
            move_line = line.move_line_id or False

            if not move_line:
                res['amount_original'] = 0.0
                res['amount_unreconciled'] = 0.0
                res['amount_withholding_tax'] = 0.0
            elif move_line.currency_id \
                    and voucher_currency == move_line.currency_id.id:
                # modify for WT
                res['amount_original'] = abs(
                    move_line.amount_currency -
                    move_line.withholding_tax_amount)
                res['amount_unreconciled'] = abs(
                    move_line.amount_residual_currency)
            else:
                # always use the amount booked in the company currency as the
                # basis of the conversion into the voucher currency
                res['amount_original'] = currency_pool.compute(
                    cr, uid, company_currency, voucher_currency,
                    move_line.credit or move_line.debit or 0.0, context=ctx)
                res['amount_unreconciled'] = currency_pool.compute(
                    cr, uid, company_currency, voucher_currency,
                    abs(move_line.amount_residual), context=ctx)
                # add for WT
                res['amount_original'] -= move_line.withholding_tax_amount

            rs_data[line.id] = res
        return rs_data

    _columns = {
        'amount_original': fields.function(
            _compute_balance, multi='dc', type='float',
            string='Original Amount', store=True,
            digits_compute=dp.get_precision('Account')),
        'amount_original_withholding_tax': fields.function(
            _amount_withholding_tax,
            digits_compute=dp.get_precision('Account'),
            string='Withholding Tax Original', multi='withholding_tax'),
        'amount_residual_withholding_tax': fields.float(
            'Withholding Tax Amount Residual'),
        'amount_withholding_tax': fields.float(
            'Withholding Tax Amount'),
        'withholding_tax_line_ids': fields.one2many(
            'withholding.tax.voucher.line', 'voucher_line_id',
            'Withholding Tax Lines'),
    }

    def onchange_amount(self, cr, uid, ids, amount, amount_unreconciled,
                        amount_residual_withholding_tax, context=None):
        res = super(AccountVoucherLine, self).onchange_amount(
            cr, uid, ids, amount, amount_unreconciled, context=context)
        dp_obj = self.pool['decimal.precision']
        wt_amount = self.compute_amount_withholdin_tax(
            cr, uid, amount, amount_unreconciled,
            amount_residual_withholding_tax, context)
        res['value'].update({'amount_withholding_tax': wt_amount})

        # Setting for Total amount
        if (amount + wt_amount) >= round(
                amount_unreconciled, dp_obj.precision_get(cr, uid, 'Account')):
            res['value'].update({'reconcile': True})
            res['value'].update({'amount': amount})

        return res

    def onchange_reconcile(self, cr, uid, ids, reconcile, amount,
                           amount_unreconciled,
                           amount_residual_withholding_tax,
                           context=None):
        """
        TO CONSIDER: Amount tot = amount net + amount WT
        """
        res = super(AccountVoucherLine, self).onchange_reconcile(
            cr, uid, ids, reconcile, amount, amount_unreconciled,
            context=context)
        if reconcile:
            amount = amount_unreconciled
            wt_amount = self.compute_amount_withholdin_tax(
                cr, uid, amount, amount_unreconciled,
                amount_residual_withholding_tax, context)
            res['value']['amount'] = amount - wt_amount
        return res

    def compute_amount_residual_withholdin_tax(
            self, cr, uid, line, context=None):
        """
        WT residual = WT amount original - (All WT amounts in voucher posted)
        """
        wt_amount_residual = 0.0
        if 'move_line_id' not in line or not line['move_line_id']:
            return wt_amount_residual
        domain = [('move_line_id', '=', line['move_line_id'])]
        v_line_ids = self.search(cr, uid, domain)
        wt_amount_residual = line['amount_original_withholding_tax']
        for v_line in self.browse(cr, uid, v_line_ids):
            if v_line.voucher_id.state == 'posted':
                wt_amount_residual -= v_line.amount_withholding_tax

        return wt_amount_residual

    def compute_amount_withholdin_tax(
            self, cr, uid, amount, amount_unreconciled, wt_amount_residual,
            context=None):
        dp_obj = self.pool['decimal.precision']
        wt_amount = 0.0
        # Total amount
        amount_tot = amount + wt_amount_residual
        base_amount = amount_unreconciled - wt_amount_residual
        if amount_tot >= round(amount_unreconciled,
                               dp_obj.precision_get(cr, uid, 'Account')):
            wt_amount = wt_amount_residual
        # Partial amount ( ratio with amount net)
        else:
            wt_amount = round(
                wt_amount_residual * (1.0 * amount / base_amount),
                dp_obj.precision_get(cr, uid, 'Account'))
        return wt_amount

    def recompute_withholding_tax_voucher_line(
            self, cr, uid, voucher_line_id, context=None):
        """
        Split amount voucher line second WT lines invoice
        """
        res = []
        invoice_obj = self.pool['account.invoice']
        wt_voucher_line_obj = self.pool['withholding.tax.voucher.line']
        dp_obj = self.pool['decimal.precision']

        voucher_line = self.browse(cr, uid, voucher_line_id)
        # delete existing wt lines
        domain = [('voucher_line_id', '=', voucher_line_id)]
        wtv_line_ids = wt_voucher_line_obj.search(cr, uid, domain)
        wt_voucher_line_obj.unlink(cr, uid, wtv_line_ids)
        #
        if voucher_line.amount_withholding_tax:
            domain = [('move_id', '=', voucher_line.move_line_id.move_id.id)]
            inv_ids = invoice_obj.search(cr, uid, domain)
            for inv in invoice_obj.browse(cr, uid, inv_ids):
                for wt_tax in inv.withholding_tax_line:
                    if len(wt_tax.filtered(lambda x: x == wt_tax)):
                        rate_num = len(wt_tax.filtered(lambda x: x == wt_tax))
                        # Rates
                        wt_amount_rate = round(
                            voucher_line.amount_withholding_tax / rate_num * (
                                wt_tax.tax / sum(
                                    x.tax for x in inv.withholding_tax_line)
                                ),
                            dp_obj.precision_get(cr, uid, 'Account'))
                        wt_residual = voucher_line.amount_withholding_tax * (
                            wt_tax.tax / sum(
                                x.tax for x in inv.withholding_tax_line)
                            )
                        # Re-read move lines to assign the amounts of wt
                        i = 0
                        for wt_invoice_line in inv.withholding_tax_line.\
                                filtered(lambda x: x == wt_tax):
                            i += 1
                            if i == rate_num:
                                wt_amount = wt_residual
                            else:
                                wt_amount = wt_amount_rate
                            wt_residual -= wt_amount

                            val = {
                                'voucher_line_id': voucher_line_id,
                                'withholding_tax_id':
                                    wt_invoice_line.withholding_tax_id.id,
                                'amount': wt_amount
                            }
                            wt_voucher_line_obj.create(cr, uid, val)

        return res

    def create(self, cr, uid, vals, *args, **kwargs):
        res_id = super(AccountVoucherLine, self).create(
            cr, uid, vals, *args, **kwargs)
        self.recompute_withholding_tax_voucher_line(
            cr, uid, res_id, context=None)
        return res_id

    def write(self, cr, uid, ids, vals, context=None):
        res = super(AccountVoucherLine, self).write(
            cr, uid, ids, vals, context)
        if 'amount_withholding_tax' in vals:
            for line_id in ids:
                self.recompute_withholding_tax_voucher_line(cr, uid, line_id)
        return res


class WithholdingTaxVoucherLine(orm.Model):
    _name = 'withholding.tax.voucher.line'
    _description = 'Withholding Tax Voucher Line'

    _columns = {
        'voucher_line_id': fields.many2one(
            'account.voucher.line', 'Account Voucher Line',
            ondelete='cascade'),
        'withholding_tax_id': fields.many2one(
            'withholding.tax', 'Withholding Tax'),
        'amount': fields.float('Amount'),
    }

    def _align_wt_move(self, cr, uid, ids, context=None):
        """
        Align with wt move lines
        """
        wt_statement_obj = self.pool['withholding.tax.statement']
        wt_move_obj = self.pool['withholding.tax.move']
        payment_term_obj = self.pool['account.payment.term']
        for wt_v_line in self.browse(cr, uid, ids):
            # Search statemnt of competence
            domain = [('move_id', '=',
                       wt_v_line.voucher_line_id.move_line_id.move_id.id),
                      ('withholding_tax_id', '=',
                       wt_v_line.withholding_tax_id.id)]
            wt_st_ids = wt_statement_obj.search(cr, uid, domain)
            if wt_st_ids:
                wt_st_id = wt_st_ids[0]
            else:
                wt_st_id = False
            # Date maturity
            # TODO : split wt moves for payment with more lines
            payment_lines = payment_term_obj.compute(
                cr, uid, wt_v_line.withholding_tax_id.payment_term.id,
                wt_v_line.amount,
                wt_v_line.voucher_line_id.voucher_id.date or False,
                context=context)
            if payment_lines:
                p_date_maturity = payment_lines[0][0]
            # Create move if doesn't exist
            domain = [('wt_voucher_line_id', '=', wt_v_line.id),
                      ('move_line_id', '=', False)]
            wt_move_ids = wt_move_obj.search(cr, uid, domain)
            wt_move_vals = {
                'statement_id': wt_st_id,
                'date': wt_v_line.voucher_line_id.voucher_id.date,
                'partner_id':
                    wt_v_line.voucher_line_id.voucher_id.partner_id.id,
                'wt_voucher_line_id': wt_v_line.id,
                'withholding_tax_id': wt_v_line.withholding_tax_id.id,
                'account_move_id':
                    wt_v_line.voucher_line_id.voucher_id.move_id.id,
                'date_maturity':
                    p_date_maturity or
                    wt_v_line.voucher_line_id.move_line_id.date_maturity
            }
            if not wt_move_ids:
                wt_move_id = wt_move_obj.create(cr, uid, wt_move_vals)
            else:
                wt_move_id = wt_move_ids[0]

            # Update values
            wt_move_vals.update({'amount': wt_v_line.amount})
            wt_move_obj.write(cr, uid, [wt_move_id], wt_move_vals)
            # wt_move.write(wt_move_vals)
        return True

    def create(self, cr, uid, vals, *args, **kwargs):
        res_id = super(WithholdingTaxVoucherLine, self).create(
            cr, uid, vals, *args, **kwargs)
        # Align with wt move
        self._align_wt_move(cr, uid, [res_id])
        return res_id

    def write(self, cr, uid, ids, vals, context=None):
        res = super(WithholdingTaxVoucherLine, self).write(
            cr, uid, ids, vals, context)
        # Align with wt move
        self._align_wt_move(cr, uid, ids)
        return res
