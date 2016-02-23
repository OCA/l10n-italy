# -*- coding: utf-8 -*-
#
#
#    OpenERP - Import operations model 347 engine
#    Copyright (C) 2009 Asr Oss. All Rights Reserved
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
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
#

"""
Create FYC entries wizards
"""

from tools.translate import _
import netsvc
from osv import osv


class wizard_run(osv.osv_memory):

    """
    Wizard to create the FYC entries.
    """

    _name = 'fyc.run'

    def run(self, cr, uid, ids, context=None):
        """
        Creates / removes FYC entries
        """

        pool = self.pool
        active_id = context and context.get('active_id', False) or False
        if not active_id:
            raise osv.except_osv(_('Error'), _('No active ID found'))
        # Read the object
        fyc = pool.get('account_fiscal_year_closing.fyc').browse(
            cr, uid, active_id, context=context)

        #
        # Check for invalid period moves if needed
        #
        if fyc.check_invalid_period_moves:
            self._check_invalid_period_moves(cr, uid, fyc, context)

        #
        # Check for draft moves if needed
        #
        if fyc.check_draft_moves:
            self._check_draft_moves(cr, uid, fyc, context)

        #
        # Check for unbalanced moves if needed
        #
        if fyc.check_unbalanced_moves:
            self._check_unbalanced_moves(cr, uid, fyc, context)

        #
        # Create L&P move if needed
        #
        if fyc.create_loss_and_profit and not fyc.loss_and_profit_move_id:
            self.create_closing_move(cr, uid, 'loss_and_profit', fyc, context)
        #
        # Remove the L&P move if needed
        #
        if (not fyc.create_loss_and_profit) and fyc.loss_and_profit_move_id:
            self.remove_move(cr, uid, 'loss_and_profit', fyc, context)

        # Refresh the cached fyc object
        fyc = pool.get('account_fiscal_year_closing.fyc').browse(
            cr, uid, active_id, context=context)

        #
        # Create the Net L&P move if needed
        #
        if (
            fyc.create_net_loss_and_profit and
            not fyc.net_loss_and_profit_move_id
        ):
            self.create_closing_move(
                cr, uid, 'net_loss_and_profit', fyc, context)
        #
        # Remove the Net L&P move if needed
        #
        if (
            not fyc.create_net_loss_and_profit
        ) and fyc.net_loss_and_profit_move_id:
            self.remove_move(cr, uid, 'net_loss_and_profit', fyc, context)

        # Refresh the cached fyc object
        fyc = pool.get('account_fiscal_year_closing.fyc').browse(
            cr, uid, active_id, context=context)

        #
        # Create the closing move if needed
        #
        if fyc.create_closing and not fyc.closing_move_id:
            self.create_closing_move(cr, uid, 'close', fyc, context)
        #
        # Remove the closing move if needed
        #
        if (not fyc.create_closing) and fyc.closing_move_id:
            self.remove_move(cr, uid, 'close', fyc, context)

        # Refresh the cached fyc object
        fyc = pool.get('account_fiscal_year_closing.fyc').browse(
            cr, uid, active_id, context=context)

        #
        # Create the opening move if needed
        #
        if fyc.create_opening and not fyc.opening_move_id:
            self.create_opening_move(cr, uid, 'open', fyc, context)
        #
        # Remove the opening move if needed
        #
        if (not fyc.create_opening) and fyc.opening_move_id:
            self.remove_move(cr, uid, 'open', fyc, context)

        #
        # Set the fyc as done (if not in cancel_mode)
        #
        if (
            not fyc.create_opening and not fyc.create_closing and
            not not fyc.create_net_loss_and_profit and
            not fyc.create_loss_and_profit
        ):
            wf_service = netsvc.LocalService("workflow")
            wf_service.trg_validate(
                uid, 'account_fiscal_year_closing.fyc', fyc.id, 'cancel', cr)
        else:
            wf_service = netsvc.LocalService("workflow")
            wf_service.trg_validate(
                uid, 'account_fiscal_year_closing.fyc', fyc.id, 'run', cr)

        return {'type': 'ir.actions.act_window_close'}

    #
    # CHECK OPERATIONS
    #

    def _check_invalid_period_moves(self, cr, uid, fyc, context):
        """
        Checks for moves with invalid period on the fiscal year that is being
        closed
        """
        pool = self.pool

        # Consider all the periods of the fiscal year.
        period_ids = [
            period.id for period in fyc.closing_fiscalyear_id.period_ids]

        # Find moves on the closing fiscal year with dates of previous years
        account_move_ids = pool.get('account.move').search(cr, uid, [
            ('period_id', 'in', period_ids),
            ('date', '<', fyc.closing_fiscalyear_id.date_start),
        ], context=context)

        # Find moves on the closing fiscal year with dates of next years
        account_move_ids.extend(pool.get('account.move').search(cr, uid, [
                                ('period_id', 'in', period_ids),
                                ('date', '>',
                                 fyc.closing_fiscalyear_id.date_stop),
                                ], context=context))

        # Find moves not on the closing fiscal year with dates on its year
        account_move_ids.extend(pool.get('account.move').search(cr, uid, [
                                ('period_id', 'not in', period_ids),
                                ('date', '>=',
                                 fyc.closing_fiscalyear_id.date_start),
                                ('date', '<=',
                                 fyc.closing_fiscalyear_id.date_stop),
                                ], context=context))

        #
        # If one or more moves where found, raise an exception
        #
        if len(account_move_ids):
            invalid_period_moves = pool.get('account.move').browse(
                cr, uid, account_move_ids, context)
            str_invalid_period_moves = '\n'.join(
                [
                    'id: %s, date: %s, number: %s, ref: %s'
                    % (move.id, move.date, move.name, move.ref)
                    for move in invalid_period_moves
                ])
            raise osv.except_osv(
                _('Error'),
                _('One or more moves with invalid period or date found on the '
                  'fiscal year: \n%s') % str_invalid_period_moves)

    def _check_draft_moves(self, cr, uid, fyc, context):
        """
        Checks for draft moves on the fiscal year that is being closed
        """
        pool = self.pool

        #
        # Consider all the periods of the fiscal year *BUT* the L&P,
        # Net L&P and the Closing one.
        #
        period_ids = []
        for period in fyc.closing_fiscalyear_id.period_ids:
            if period.id != fyc.lp_period_id.id and \
                    period.id != fyc.nlp_period_id.id and \
                    period.id != fyc.c_period_id.id:
                period_ids.append(period.id)

        # Find the moves on the given periods
        account_move_ids = pool.get('account.move').search(cr, uid, [
            ('period_id', 'in', period_ids),
            ('state', '=', 'draft'),
        ], context=context)

        #
        # If one or more draft moves where found, raise an exception
        #
        if len(account_move_ids):
            draft_moves = pool.get('account.move').browse(
                cr, uid, account_move_ids, context)
            str_draft_moves = '\n'.join(
                [
                    'id: %s, date: %s, number: %s, ref: %s'
                    % (move.id, move.date, move.name, move.ref)
                    for move in draft_moves
                ])
            raise osv.except_osv(
                _('Error'),
                _('One or more draft moves found: \n%s') % str_draft_moves)

    def _check_unbalanced_moves(self, cr, uid, fyc, context):
        """
        Checks for unbalanced moves on the fiscal year that is being closed
        """
        pool = self.pool

        #
        # Consider all the periods of the fiscal year *BUT* the L&P,
        # Net L&P and the Closing one.
        #
        period_ids = []
        for period in fyc.closing_fiscalyear_id.period_ids:
            if period.id != fyc.lp_period_id.id and \
                    period.id != fyc.nlp_period_id.id and \
                    period.id != fyc.c_period_id.id:
                period_ids.append(period.id)

        # Find the moves on the given periods
        account_move_ids = pool.get('account.move').search(cr, uid, [
            ('period_id', 'in', period_ids),
            ('state', '!=', 'draft'),
        ], context=context)

        #
        # For each found move, check it
        #
        unbalanced_moves = []
        for move in pool.get('account.move').browse(
            cr, uid, account_move_ids, context
        ):
            amount = 0
            for line in move.line_id:
                amount += (line.debit - line.credit)

            if round(abs(amount), pool.get('decimal.precision').precision_get(
                cr, uid, 'Account'
            )) > 0:
                unbalanced_moves.append(move)

        #
        # If one or more unbalanced moves where found, raise an exception
        #
        if len(unbalanced_moves):
            str_unbalanced_moves = '\n'.join(
                [
                    'id: %s, date: %s, number: %s, ref: %s'
                    % (move.id, move.date, move.name, move.ref)
                    for move in unbalanced_moves
                ])
            raise osv.except_osv(
                _('Error'),
                _('One or more unbalanced moves found: \n%s')
                % str_unbalanced_moves)

    #
    # CLOSING/OPENING OPERATIONS
    #

    def create_closing_move(self, cr, uid, operation, fyc, context):
        """
        Create a closing move (L&P, NL&P or Closing move).
        """
        pool = self.pool

        move_lines = []
        dest_accounts_totals = {}
        period_ids = []
        for period in fyc.closing_fiscalyear_id.period_ids:
            period_ids.append(period.id)
        account_mapping_ids = []
        description = None
        date = None
        period_id = None
        journal_id = None

        #
        # Depending on the operation we will use different data
        #
        if operation == 'loss_and_profit':
            #
            # Set the accounts to use
            #
            account_mapping_ids = fyc.lp_account_mapping_ids
            for account_map in account_mapping_ids:
                if not account_map.dest_account_id:
                    raise osv.except_osv(
                        _('UserError'),
                        _("The L&P account mappings are not properly "
                          "configured: %s") % account_map.name)

            #
            # Get the values for the lines
            #
            if not fyc.lp_description:
                raise osv.except_osv(
                    _('UserError'), _("The L&P description must be defined"))
            if not fyc.lp_date:
                raise osv.except_osv(
                    _('UserError'), _("The L&P date must be defined"))
            if not (fyc.lp_period_id and fyc.lp_period_id.id):
                raise osv.except_osv(
                    _('UserError'), _("The L&P period must be defined"))
            if not (fyc.lp_journal_id and fyc.lp_journal_id.id):
                raise osv.except_osv(
                    _('UserError'), _("The L&P journal must be defined"))
            description = fyc.lp_description
            date = fyc.lp_date
            period_id = fyc.lp_period_id.id
            journal_id = fyc.lp_journal_id.id
        elif operation == 'net_loss_and_profit':
            #
            # Set the accounts to use
            #
            account_mapping_ids = fyc.nlp_account_mapping_ids
            #
            # Get the values for the lines
            #
            if not fyc.nlp_description:
                raise osv.except_osv(
                    _('UserError'),
                    _("The Net L&P description must be defined"))
            if not fyc.nlp_date:
                raise osv.except_osv(
                    _('UserError'), _("The Net L&P date must be defined"))
            if not (fyc.nlp_period_id and fyc.nlp_period_id.id):
                raise osv.except_osv(
                    _('UserError'), _("The Net L&P period must be defined"))
            if not (fyc.nlp_journal_id and fyc.nlp_journal_id.id):
                raise osv.except_osv(
                    _('UserError'), _("The Net L&P journal must be defined"))
            description = fyc.nlp_description
            date = fyc.nlp_date
            period_id = fyc.nlp_period_id.id
            journal_id = fyc.nlp_journal_id.id
        elif operation == 'close':
            # Require the user to have performed the L&P operation
            if not (
                fyc.loss_and_profit_move_id and fyc.loss_and_profit_move_id.id
            ):
                raise osv.except_osv(
                    _('UserError'),
                    _("The L&P move must exist before creating the closing "
                      "one"))
            # Set the accounts to use
            account_mapping_ids = fyc.c_account_mapping_ids
            #
            # Get the values for the lines
            #
            if not fyc.c_description:
                raise osv.except_osv(
                    _('UserError'),
                    _("The closing description must be defined"))
            if not fyc.c_date:
                raise osv.except_osv(
                    _('UserError'), _("The closing date must be defined"))
            if not (fyc.c_period_id and fyc.c_period_id.id):
                raise osv.except_osv(
                    _('UserError'), _("The closing period must be defined"))
            if not (fyc.c_journal_id and fyc.c_journal_id.id):
                raise osv.except_osv(
                    _('UserError'), _("The closing journal must be defined"))
            description = fyc.c_description
            date = fyc.c_date
            period_id = fyc.c_period_id.id
            journal_id = fyc.c_journal_id.id
        else:
            assert operation in (
                'loss_and_profit', 'net_loss_and_profit', 'close'
            ), "The operation must be a supported one"

        #
        # For each (parent) account in the mapping list
        #
        accounts_done = 0
        for account_map in account_mapping_ids:
            # Init (if needed) the dictionary that will store the totals for
            # the dest accounts
            if account_map.dest_account_id:
                dest_accounts_totals[
                    account_map.dest_account_id.id
                ] = dest_accounts_totals.get(
                    account_map.dest_account_id.id, 0)

            context.update({'periods': period_ids})
            ctx = context.copy()

            # Find its children accounts (recursively)
            # FIXME: _get_children_and_consol is a protected member of
            # account_account but the OpenERP code base uses it like this :(
            child_ids = pool.get('account.account')._get_children_and_consol(
                cr, uid, [account_map.source_account_id.id], ctx)

            # For each children account. (Notice the context filter! the
            # computed balanced is based on this filter)
            for account in pool.get('account.account').browse(
                cr, uid, child_ids, ctx
            ):
                # Check if the children account needs to (and can) be closed
                # Note: We currently ignore the close_method
                # (account.user_type.close_method)
                #       and always do a balance close.
                if account.type != 'view':
                    # Compute the balance for the account (uses the previous
                    # browse context filter)
                    balance = account.balance
                    # Check if the balance is greater than the limit
                    if round(abs(balance), pool.get(
                        'decimal.precision'
                    ).precision_get(cr, uid, 'Account')) > 0:
                        #
                        # Add a new line to the move
                        #
                        move_lines.append({
                            'account_id': account.id,
                            'debit': balance < 0 and -balance,
                            'credit': balance > 0 and balance,
                            'name': description,
                            'date': date,
                            'period_id': period_id,
                            'journal_id': journal_id,
                        })

                        # Update the dest account total (with the inverse of
                        # the balance)
                        if account_map.dest_account_id:
                            dest_accounts_totals[
                                account_map.dest_account_id.id] -= balance
            accounts_done += 1

        #
        # Add the dest lines
        #
        for dest_account_id in dest_accounts_totals.keys():
            balance = dest_accounts_totals[dest_account_id]
            move_lines.append({
                'account_id': dest_account_id,
                'debit': balance < 0 and -balance,
                'credit': balance > 0 and balance,
                'name': description,
                'date': date,
                'period_id': period_id,
                'journal_id': journal_id,
            })

        #
        # Finally create the account move with all the lines (if needed)
        #
        if len(move_lines):
            move_id = pool.get('account.move').create(cr, uid, {
                'ref': description,
                'date': date,
                'period_id': period_id,
                'journal_id': journal_id,
                'line_id': [(0, 0, line) for line in move_lines],
            }, context=context)
            # pool.get('account.move').button_validate(cr, uid, [move_id],
            # context)
        else:
            move_id = None

        #
        # Save the reference to the created account move into the fyc object
        #
        if operation == 'loss_and_profit':
            pool.get('account_fiscal_year_closing.fyc').write(
                cr, uid, [fyc.id], {'loss_and_profit_move_id': move_id})
        elif operation == 'net_loss_and_profit':
            pool.get('account_fiscal_year_closing.fyc').write(
                cr, uid, [fyc.id], {'net_loss_and_profit_move_id': move_id})
        elif operation == 'close':
            pool.get('account_fiscal_year_closing.fyc').write(
                cr, uid, [fyc.id], {'closing_move_id': move_id})
        else:
            assert operation in (
                'loss_and_profit', 'net_loss_and_profit', 'close'
            ), "The operation must be a supported one"

        return move_id

    def create_opening_move(self, cr, uid, operation, fyc, context):
        """
        Create an opening move (based on the closing one)
        """
        pool = self.pool

        move_lines = []
        description = None
        date = None
        period_id = None
        journal_id = None
        closing_move = None

        #
        # Depending on the operation we will use one or other closing move
        # as the base for the opening move.
        # Note: Yes, currently only one 'closing' move exists,
        #       but I want this to be extensible :)
        #
        if operation == 'open':
            closing_move = fyc.closing_move_id
            # Require the user to have performed the closing operation
            if not (closing_move and closing_move.id):
                raise osv.except_osv(
                    _('UserError'),
                    _("The closing move must exist to create the opening one"))
            if not closing_move.line_id:
                raise osv.except_osv(
                    _('UserError'), _("The closing move shouldn't be empty"))
            #
            # Get the values for the lines
            #
            if not fyc.o_description:
                raise osv.except_osv(
                    _('UserError'),
                    _("The opening description must be defined"))
            if not fyc.o_date:
                raise osv.except_osv(
                    _('UserError'), _("The opening date must be defined"))
            if not (fyc.o_period_id and fyc.o_period_id.id):
                raise osv.except_osv(
                    _('UserError'), _("The opening period must be defined"))
            if not (fyc.o_journal_id and fyc.o_journal_id.id):
                raise osv.except_osv(
                    _('UserError'), _("The opening journal must be defined"))
            description = fyc.o_description
            date = fyc.o_date
            period_id = fyc.o_period_id.id
            journal_id = fyc.o_journal_id.id
        else:
            assert operation in (
                'open'), "The operation must be a supported one"

        #
        # Read the lines from the closing move, and append the inverse lines
        # to the opening move lines.
        #
        accounts_done = 0
        for line in closing_move.line_id:
            move_lines.append({
                'account_id': line.account_id.id,
                'debit': line.credit,
                'credit': line.debit,
                'name': description,
                'date': date,
                'period_id': period_id,
                'journal_id': journal_id,
            })
            accounts_done += 1

        #
        # Finally create the account move with all the lines (if needed)
        #
        if len(move_lines):
            move_id = pool.get('account.move').create(cr, uid, {
                'ref': description,
                'date': date,
                'period_id': period_id,
                'journal_id': journal_id,
                'line_id': [(0, 0, line) for line in move_lines],
            }, context=context)
            # pool.get('account.move').button_validate(cr, uid, [move_id],
            # context)
        else:
            move_id = None

        #
        # Save the reference to the created account move into the fyc object
        #
        if operation == 'open':
            pool.get('account_fiscal_year_closing.fyc').write(
                cr, uid, [fyc.id], {'opening_move_id': move_id})
        else:
            assert operation in (
                'open'), "The operation must be a supported one"

        return move_id

    def remove_move(self, cr, uid, operation, fyc, context):
        """
        Remove a account move (L&P, NL&P, Closing or Opening move)
        """
        pool = self.pool

        #
        # Depending on the operation we will delete one or other move
        #
        move = None
        if operation == 'loss_and_profit':
            move = fyc.loss_and_profit_move_id
            pool.get('account_fiscal_year_closing.fyc').write(
                cr, uid, fyc.id, {'loss_and_profit_move_id': None})
        elif operation == 'net_loss_and_profit':
            move = fyc.net_loss_and_profit_move_id
            pool.get('account_fiscal_year_closing.fyc').write(
                cr, uid, fyc.id, {'net_loss_and_profit_move_id': None})
        elif operation == 'close':
            move = fyc.closing_move_id
            pool.get('account_fiscal_year_closing.fyc').write(
                cr, uid, fyc.id, {'closing_move_id': None})
        elif operation == 'open':
            move = fyc.opening_move_id
            pool.get('account_fiscal_year_closing.fyc').write(
                cr, uid, fyc.id, {'opening_move_id': None})
        else:
            assert operation in (
                'loss_and_profit', 'net_loss_and_profit',
                'close', 'open'), "The operation must be a supported one"

        assert move and move.id, "The move to delete must be defined"

        pool.get('account.move').unlink(cr, uid, [move.id], context)

        return move.id
