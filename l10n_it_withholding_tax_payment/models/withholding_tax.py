# -*- coding: utf-8 -*-
# Copyright © 2015 Alessandro Camilli (<http://www.openforce.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp.osv import orm, fields
from openerp.tools.translate import _
from openerp.exceptions import ValidationError
from openerp import workflow
from datetime import datetime


class WithholdingTaxMove(orm.Model):
    _inherit = 'withholding.tax.move'
    _columns = {
        'wt_move_payment_id': fields.many2one(
            'withholding.tax.move.payment', 'Move Payment', readonly=True,),
    }

    def unlink(self, cr, uid, ids, context=None):
        for rec in self.browse(cr, uid, ids, context):
            if rec.wt_move_payment_id:
                raise ValidationError(
                    _(('Warning! Withholding tax move in payment %s: \
                    you can not delete it') % rec.wt_move_payment_id.name))
        return super(WithholdingTaxMove, self).unlink(
            cr, uid, ids, context)


class WithholdingTaxMovePayment(orm.Model):
    _name = 'withholding.tax.move.payment'
    _description = 'Withholding Tax Move Payment'

    def _get_current_statement(self, cr, uid, ids, name, context=None):
        statement_ids = []
        line_obj = self.pool['withholding.tax.move']
        for move in line_obj.browse(cr, uid, ids, context=context):
            statement_ids.append(move.wt_move_payment_id.id)
        return statement_ids

    def _compute_total(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            tot_wt_amount = 0
            for wt_move in line.line_ids:
                tot_wt_amount += wt_move.amount
            res[line.id] = {
                'amount': tot_wt_amount,
            }
        return res

    _columns = {
        'state': fields.selection([
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
        ], 'Status', readonly=True, copy=False, select=True),
        'name': fields.char('Name'),
        'date': fields.date('Date'),
        'date_payment': fields.date('Date Payment'),
        'date_start': fields.date('Date Start', readonly=True),
        'date_stop': fields.date('Date Stop', readonly=True),
        'move_id': fields.many2one('account.move', 'Account move', readonly=True),
        'account_id': fields.many2one('account.account', 'Account'),
        'journal_id': fields.many2one('account.journal', 'Journal'),
        'line_ids': fields.one2many('withholding.tax.move',
                                    'wt_move_payment_id',
                                    string='Lines',
                                    ),
        'amount': fields.function(_compute_total,
                                  string='WT amount', multi='total',
                                  store={'withholding.tax.move': (
                                      _get_current_statement,
                                      ['amount', 'wt_move_payment_id'],
                                      20),
                                  },),
    }

    _defaults = {
        'state': 'draft'
    }

    def generate_from_moves(self, cr, uid, move_ids, context=None):
        res_id = False
        wt_move_obj = self.pool['withholding.tax.move']
        sequence_obj = self.pool['ir.sequence']
        wt_moves = []
        for wt_move in wt_move_obj.browse(cr, uid, move_ids):
            if wt_move.state == 'paid':
                raise orm.except_orm(_('Error!'),
                                     _("Wt move already paid! - %s - %s - %s")
                                     % (wt_move.partner_id.name,
                                        wt_move.date,
                                        str(wt_move.amount)))
            if wt_move.wt_move_payment_id:
                raise orm.except_orm(_('Error!'),
                                     _("Wt move already in a move payment! \
                        Move paym. %s -Ref WT: %s - %s - %s")
                                     % (str(wt_move.wt_move_payment_id.id),
                                        wt_move.partner_id.name,
                                        wt_move.date,
                                        str(wt_move.amount)))
            wt_moves.append(wt_move.id)
        # DA FARE -> passare altri dati di testata su context
        if wt_moves:
            # Create Move payment
            val = {
                'name': sequence_obj.get(cr, uid,
                                         'withholding.tax.move.payment'),
                'date': datetime.today(),
                'line_ids': [(6, 0, wt_moves)]
            }
            res_id = self.create(cr, uid, val)
            # Update ref on moves
            wt_move_obj.write(cr, uid, wt_moves,
                              {'wt_move_payment_id': res_id})
        return res_id

    def create_account_move(self, cr, uid, ids, context=None):
        period_obj = self.pool['account.period']
        account_move_obj = self.pool['account.move']
        account_move_line_obj = self.pool['account.move.line']

        for mp in self.browse(cr, uid, ids):
            # controls field for move creation
            if not mp.date_payment \
                    or not mp.journal_id\
                    or not mp.account_id:
                raise orm.except_orm(_('Error!'),
                                     _("Datas required for account move creation: \
                        Date payment, journal, account"))
            # Period
            period_ids = period_obj.find(cr, uid, mp.date_payment,
                                         context=None)
            period_id = period_ids and period_ids[0] or False
            # Head Move
            move_id = account_move_obj.create(cr, uid, {
                'ref': _('Withholding Tax Payment'),
                'journal_id': mp.journal_id.id,
                'date': mp.date_payment,
                'period_id': period_id
            }, context=context)
            # WT Moves
            wt_move_balance = 0
            for wt_move in mp.line_ids:
                debit = 0
                credit = 0
                if wt_move.amount > 0:
                    debit = wt_move.amount
                else:
                    credit = wt_move.amount

                account_move_line_obj.create(cr, uid, {
                    'name': _('Withholding Tax Payment %s')
                    % wt_move.partner_id.name,
                    'account_id':
                        wt_move.withholding_tax_id.account_payable_id.id,
                    'credit': credit,
                    'debit': debit,
                    'move_id': move_id,
                }, context=context)
                # Balance
                wt_move_balance += wt_move.amount
            # WT payment
            if wt_move_balance:
                debit = 0
                credit = 0
                if wt_move_balance > 0:
                    credit = wt_move_balance
                else:
                    debit = wt_move_balance * -1

                account_move_line_obj.create(cr, uid, {
                    'name': _('Withholding Tax Payment'),
                    'account_id': mp.account_id.id,
                    'credit': credit,
                    'debit': debit,
                    'move_id': move_id,
                }, context=context)
            # Update ref account move
            self.write(cr, uid, [mp.id], {'move_id': move_id})

        return True

    def action_confirmed(self, cr, uid, ids, context=None):
        for res_id in ids:
            workflow.trg_validate(uid, self._name, res_id, 'confirmed', cr)
        return True

    def action_set_to_draft(self, cr, uid, ids, context=None):
        for res_id in ids:
            workflow.trg_validate(uid, self._name, res_id, 'cancel', cr)
        return True

    def move_payment_to_draft(self, cr, uid, ids, *args):
        wt_move_obj = self.pool['withholding.tax.move']
        for move in self.browse(cr, uid, ids):
            if move.state in ['confirmed']:
                self.write(cr, uid, [move.id], {'state': 'draft'})
                # Wt move set to due
                for wt_move in move.line_ids:
                    wt_move_obj.action_set_to_draft(cr, uid,
                                                    [wt_move.id])

        return True

    def move_payment_confirmed(self, cr, uid, ids, *args):
        wt_move_obj = self.pool['withholding.tax.move']
        for move in self.browse(cr, uid, ids):
            if move.state in ['draft']:
                self.write(cr, uid, [move.id], {'state': 'confirmed'})
                # Wt move set to paid
                for wt_move in move.line_ids:
                    wt_move_obj.action_paid(cr, uid, [wt_move.id])

        return True

    def unlink(self, cr, uid, ids, context=None):
        for payment in self.browse(cr, uid, ids, context):
            if payment.state != 'draft':
                raise ValidationError(_("You can only delete draft payments"))
            if payment.move_id:
                raise ValidationError(_("You cannot delete payments %s because "
                                        "an account moves is linked to it.\n"
                                        "Try to cancel and delete it first, "
                                        "then retry.")
                                      % payment.name)
        return super(WithholdingTaxMovePayment, self).unlink(
            cr, uid, ids, context)
