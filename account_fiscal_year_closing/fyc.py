# -*- coding: utf-8 -*-
#
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 Pexego Sistemas Informáticos. All Rights Reserved
#    Copyright (C) 2011 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
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
Fiscal Year Closing
"""

from osv import fields, osv
from tools.translate import _
from datetime import datetime
import netsvc

__author__ = "Borja López Soilán (Pexego)"

# -----------------------------------------------------------------------------
# Predeclaration of the FYC object
# -------------------------------------------------------------------------


class fiscal_year_closing_init(osv.osv):

    """
    Fiscal Year Closing Wizard
    """

    _name = "account_fiscal_year_closing.fyc"
    _description = "Fiscal Year Closing Wizard"

    _columns = {
        'name': fields.char('Description', size=60, required=True),
    }


fiscal_year_closing_init()


# -----------------------------------------------------------------------------
# Account mapping objects (to be used on the fyc configuration)
# -------------------------------------------------------------------------

class fiscal_year_closing_lp_account_mapping(osv.osv):

    """
    Loss & Profit Account Mapping
    """

    _name = "account_fiscal_year_closing.fyc_lp_account_map"
    _description = "SFYC Loss & Profit Account Mapping"

    _columns = {
        'name': fields.char('Description', size=60, required=False),

        # Parent eoy
        'fyc_id': fields.many2one(
            'account_fiscal_year_closing.fyc', 'Fiscal Year Closing',
            ondelete='cascade', required=True, select=1),

        # Accounts
        'source_account_id': fields.many2one(
            'account.account', 'Source account', required=True,
            ondelete='cascade'),
        'dest_account_id': fields.many2one(
            'account.account', 'Dest account', required=False,
            ondelete='cascade'),
    }


fiscal_year_closing_lp_account_mapping()


class fiscal_year_closing_nlp_account_mapping(osv.osv):

    """
    Net Loss & Profit Account Mapping
    """

    _name = "account_fiscal_year_closing.fyc_nlp_account_map"
    _description = "SFYC Net Loss & Profit Account Mapping"

    _columns = {
        'name': fields.char('Description', size=60, required=False),

        # Parent eoy
        'fyc_id': fields.many2one(
            'account_fiscal_year_closing.fyc', 'Fiscal Year Closing',
            ondelete='cascade', required=True, select=1),

        # Accounts
        'source_account_id': fields.many2one(
            'account.account', 'Source account', required=True,
            ondelete='cascade'),
        'dest_account_id': fields.many2one(
            'account.account', 'Dest account', required=False,
            ondelete='cascade'),
    }


fiscal_year_closing_nlp_account_mapping()


class fiscal_year_closing_c_account_mapping(osv.osv):

    """
    Closing Account Mapping
    """

    _name = "account_fiscal_year_closing.fyc_c_account_map"
    _description = "SFYC Closing Account Mapping"

    _columns = {
        'name': fields.char('Description', size=60, required=False),

        # Parent eoy
        'fyc_id': fields.many2one(
            'account_fiscal_year_closing.fyc', 'Fiscal Year Closing',
            ondelete='cascade', required=True, select=1),

        # Accounts
        'source_account_id': fields.many2one(
            'account.account', 'Account', required=True, ondelete='cascade'),
        'dest_account_id': fields.many2one(
            'account.account', 'Dest account', ondelete='cascade'),
    }


fiscal_year_closing_c_account_mapping()

# -----------------------------------------------------------------------------
# Fiscal Year Closing Wizard
# -------------------------------------------------------------------------


class fiscal_year_closing(osv.osv):

    """
    Fiscal Year Closing Wizard
    """

    _inherit = "account_fiscal_year_closing.fyc"

    #
    # Fields ------------------------------------------------------------------
    #

    _columns = {
        # Company
        'company_id': fields.many2one(
            'res.company', 'Company', ondelete='cascade', readonly=True,
            required=True),

        # Fiscal years
        'closing_fiscalyear_id': fields.many2one(
            'account.fiscalyear', 'Fiscal year to close', required=True,
            ondelete='cascade', select=1),
        'opening_fiscalyear_id': fields.many2one(
            'account.fiscalyear', 'Fiscal year to open', required=True,
            ondelete='cascade', select=2),

        #
        # Operations (to do), and their account moves (when done)
        #
        'create_loss_and_profit': fields.boolean('Create Loss & Profit move'),
        'loss_and_profit_move_id': fields.many2one(
            'account.move', 'L&P Move', ondelete='set null', readonly=True),
        'create_net_loss_and_profit': fields.boolean(
            'Create Net Loss & Profit'),
        'net_loss_and_profit_move_id': fields.many2one(
            'account.move', 'Net L&P Move', ondelete='set null',
            readonly=True),
        'create_closing': fields.boolean('Close fiscal year'),
        'closing_move_id': fields.many2one(
            'account.move', 'Closing Move', ondelete='set null',
            readonly=True),
        'create_opening': fields.boolean('Open next fiscal year'),
        'opening_move_id': fields.many2one(
            'account.move', 'Opening Move', ondelete='set null',
            readonly=True),

        #
        # Extra operations
        #
        'check_invalid_period_moves': fields.boolean(
            'Check invalid period or date moves',
            help="Checks that there are no moves, on the fiscal year that is "
                 "being closed, with dates or periods outside that fiscal "
                 "year."),
        'check_draft_moves': fields.boolean(
            'Check draft moves',
            help="Checks that there are no draft moves on the fiscal year that"
                 " is being closed. Non-confirmed moves won't be taken in "
                 "account on the closing operations."),
        'check_unbalanced_moves': fields.boolean(
            'Check unbalanced moves',
            help="Checks that there are no unbalanced moves on the fiscal year"
                 " that is being closed."),

        # State
        'state': fields.selection([
                                  ('new', 'New'),
                                  ('draft', 'Draft'),
                                  ('in_progress', 'In Progress'),
                                  ('done', 'Done'),
                                  ('canceled', 'Canceled'),
                                  ], 'Status'),

        #
        # Loss and Profit options
        #
        'lp_description': fields.char('Description', size=60),
        'lp_journal_id': fields.many2one('account.journal', 'Journal'),
        'lp_period_id': fields.many2one('account.period', 'Period'),
        'lp_date': fields.date('Date'),
        'lp_account_mapping_ids': fields.one2many(
            'account_fiscal_year_closing.fyc_lp_account_map', 'fyc_id',
            'Account mappings'),

        #
        # Net Loss and Profit options
        #
        'nlp_description': fields.char('Description', size=60),
        'nlp_journal_id': fields.many2one('account.journal', 'Journal'),
        'nlp_period_id': fields.many2one('account.period', 'Period'),
        'nlp_date': fields.date('Date'),
        'nlp_account_mapping_ids': fields.one2many(
            'account_fiscal_year_closing.fyc_nlp_account_map', 'fyc_id',
            'Account mappings'),

        #
        # Closing options
        #
        'c_description': fields.char('Description', size=60),
        'c_journal_id': fields.many2one('account.journal', 'Journal'),
        'c_period_id': fields.many2one('account.period', 'Period'),
        'c_date': fields.date('Date'),
        'c_account_mapping_ids': fields.one2many(
            'account_fiscal_year_closing.fyc_c_account_map', 'fyc_id',
            'Accounts'),

        #
        # Opening options
        #
        'o_description': fields.char('Description', size=60),
        'o_journal_id': fields.many2one('account.journal', 'Journal'),
        'o_period_id': fields.many2one('account.period', 'Period'),
        'o_date': fields.date('Date'),
    }

    #
    # Default values ----------------------------------------------------------
    #

    def _get_closing_fiscalyear_id(self, cr, uid, context):
        """
        Gets the last (previous) fiscal year
        """
        company = self.pool.get('res.users').browse(
            cr, uid, uid, context).company_id
        str_date = '%s-06-01' % (datetime.now().year - 1)
        fiscalyear_ids = self.pool.get('account.fiscalyear').search(cr, uid, [
            ('company_id', '=', company.id),
            ('date_start', '<=', str_date),
            ('date_stop', '>=', str_date),
        ])
        if not fiscalyear_ids:
            fiscalyear_ids = self.pool.get('account.fiscalyear').search(
                cr, uid, [
                    ('company_id', '=', False),
                    ('date_start', '<=', str_date),
                    ('date_stop', '>=', str_date),
                ])
        return fiscalyear_ids and fiscalyear_ids[0]

    def _get_opening_fiscalyear_id(self, cr, uid, context):
        """
        Gets the current fiscal year
        """
        company = self.pool.get('res.users').browse(
            cr, uid, uid, context).company_id
        str_date = '%s-06-01' % datetime.now().year
        fiscalyear_ids = self.pool.get('account.fiscalyear').search(cr, uid, [
            ('company_id', '=', company.id),
            ('date_start', '<=', str_date),
            ('date_stop', '>=', str_date),
        ])
        if not fiscalyear_ids:
            fiscalyear_ids = self.pool.get('account.fiscalyear').search(
                cr, uid, [
                    ('company_id', '=', False),
                    ('date_start', '<=', str_date),
                    ('date_stop', '>=', str_date),
                ])
        return fiscalyear_ids and fiscalyear_ids[0]

    _defaults = {
        # Current company by default:
        'company_id': lambda self, cr, uid, context: self.pool.get(
            'res.users').browse(cr, uid, uid, context).company_id.id,

        # Draft state by default:
        'state': lambda *a: 'new',

        # Name
        'name': lambda self, cr, uid, context: _(
            "%s Fiscal Year Closing") % (datetime.now().year - 1),

        # Fiscal years
        'closing_fiscalyear_id': _get_closing_fiscalyear_id,
        'opening_fiscalyear_id': _get_opening_fiscalyear_id,
    }

    #
    # Workflow actions --------------------------------------------------------
    #

    def _get_journal_id(self, cr, uid, fyc, context):
        """
        Gets the journal to use.
        (It will search for a 'GRAL' or 'General' journal)
        """
        assert fyc.company_id, "A company should have been selected"
        journal_ids = self.pool.get('account.journal').search(cr, uid, [
            ('company_id', '=', fyc.company_id.id),
            ('code', '=', 'GRAL'),
        ])
        if not journal_ids:
            journal_ids = self.pool.get('account.journal').search(cr, uid, [
                ('company_id', '=', False),
                ('code', '=', 'GRAL'),
            ])
        if not journal_ids:
            journal_ids = self.pool.get('account.journal').search(cr, uid, [
                ('company_id', '=', fyc.company_id.id),
                ('name', 'ilike', 'General'),
            ])
        if not journal_ids:
            journal_ids = self.pool.get('account.journal').search(cr, uid, [
                ('company_id', '=', False),
                ('name', 'ilike', 'General'),
            ])
        return journal_ids and journal_ids[0]

    def _get_lp_period_id(self, cr, uid, fyc, context):
        """
        Gets the period for the L&P entry
        (It searches for a "PG%" special period on the previous fiscal year)
        """
        period_ids = self.pool.get('account.period').search(cr, uid, [
            ('fiscalyear_id', '=',
             fyc.closing_fiscalyear_id.id),
            ('special', '=', True),
            ('date_start', '=',
             fyc.closing_fiscalyear_id.date_stop),
            ('code', 'ilike', 'PG'),
        ])
        if not period_ids:
            period_ids = self.pool.get('account.period').search(cr, uid, [
                ('fiscalyear_id', '=',
                 fyc.closing_fiscalyear_id.id),
                ('special', '=', True),
                ('date_start', '=',
                 fyc.closing_fiscalyear_id.date_stop),
            ])
        return period_ids and period_ids[0]

    def _get_c_period_id(self, cr, uid, fyc, context):
        """
        Gets the period for the Closing entry
        (It searches for a "C%" special period on the previous fiscal year)
        """
        period_ids = self.pool.get('account.period').search(cr, uid, [
            ('fiscalyear_id', '=',
             fyc.closing_fiscalyear_id.id),
            ('special', '=', True),
            ('date_start', '=',
             fyc.closing_fiscalyear_id.date_stop),
            ('code', 'ilike', 'C'),
        ])

        if not period_ids:
            period_ids = self.pool.get('account.period').search(cr, uid, [
                ('fiscalyear_id', '=',
                 fyc.closing_fiscalyear_id.id),
                ('special', '=', True),
                ('date_start', '=',
                 fyc.closing_fiscalyear_id.date_stop),
            ])
        return period_ids and period_ids[0]

    def _get_o_period_id(self, cr, uid, fyc, context):
        """
        Gets the period for the Opening entry
        (It searches for a "A%" special period on the previous fiscal year)
        """
        period_ids = self.pool.get('account.period').search(cr, uid, [
            ('fiscalyear_id', '=',
             fyc.opening_fiscalyear_id.id),
            ('special', '=', True),
            ('date_stop', '=',
             fyc.opening_fiscalyear_id.date_start),
            ('code', 'ilike', 'A'),
        ])
        if not period_ids:
            period_ids = self.pool.get('account.period').search(cr, uid, [
                ('fiscalyear_id', '=',
                 fyc.opening_fiscalyear_id.id),
                ('special', '=', True),
                ('date_stop', '=',
                 fyc.opening_fiscalyear_id.date_start),
            ])
        return period_ids and period_ids[0]

    def _get_account_mappings(self, cr, uid, fyc, mapping, context):
        """
        Transforms the mapping dictionary on a list of mapping lines.
        """
        account_mappings = []
        for source, dest, description in mapping:
            #
            # Find the source account
            #
            account_ids = self.pool.get('account.account').search(cr, uid, [
                ('company_id', '=', fyc.company_id.id),
                ('code', '=like', source),
            ])
            source_account_id = account_ids and account_ids[0] or None

            #
            # Find the dest account
            #
            account_ids = self.pool.get('account.account').search(cr, uid, [
                ('company_id', '=', fyc.company_id.id),
                ('code', '=like', dest),
                ('type', '!=', 'view'),
            ])
            dest_account_id = account_ids and account_ids[0] or None

            #
            # Use a default description if not provided
            #
            if not description:
                if source_account_id:
                    description = self.pool.get('account.account').read(
                        cr, uid, source_account_id, ['name'])['name']

            #
            # If the mapping is valid for this chart of accounts
            #
            if source_account_id:
                #
                # Make sure that the dest account is valid
                #
                if dest_account_id:
                    # Add the line to the result
                    account_mappings.append({
                        'name': description,
                        'source_account_id': source_account_id,
                        'dest_account_id': dest_account_id,
                    })
                else:
                    # Add the line to the result
                    account_mappings.append({
                        'name':
                            _(
                                'No destination account %s found for account '
                                '%s.'
                            ) % (dest, source),
                        'source_account_id': source_account_id,
                        'dest_account_id': None,
                    })

        return [(0, 0, acc_map) for acc_map in account_mappings]

    def action_draft(self, cr, uid, ids, context=None):
        """
        Called when the user clicks the confirm button.
        """
        if context is None:
            context = {}
        #
        # Make sure the lang is defined on the context
        #
        user = self.pool.get('res.users').browse(cr, uid, uid, context)
        context['lang'] = context.get('lang') or user.lang

        for fyc in self.browse(cr, uid, ids, context):
            #
            # Check for duplicated entries
            #
            fyc_ids = self.search(cr, uid, [('name', '=', fyc.name)])
            if len(fyc_ids) > 1:
                raise osv.except_osv(
                    _('Error'),
                    _('There is already a fiscal year closing with this name.')
                )

            assert fyc.closing_fiscalyear_id and fyc.closing_fiscalyear_id.id
            fyc_ids = self.search(
                cr, uid,
                [('closing_fiscalyear_id', '=', fyc.closing_fiscalyear_id.id)])
            if len(fyc_ids) > 1:
                raise osv.except_osv(
                    _('Error'),
                    _('There is already a fiscal year closing for the fiscal '
                      'year to close.'))

            assert fyc.opening_fiscalyear_id and fyc.opening_fiscalyear_id.id
            fyc_ids = self.search(
                cr, uid,
                [('opening_fiscalyear_id', '=', fyc.opening_fiscalyear_id.id)])
            if len(fyc_ids) > 1:
                raise osv.except_osv(
                    _('Error'),
                    _('There is already a fiscal year closing for the fiscal '
                      'year to open.'))

            #
            # Check whether the default values of the fyc object have to be
            # computed
            # or they have already been computed (restarted workflow)
            #
            if fyc.c_account_mapping_ids:
                # Fyc wizard reverted to 'new' after canceled

                self.write(cr, uid, [fyc.id], {'state': 'draft'})
            else:
                # New fyc wizard object

                vals = {
                    #
                    # Perform all the operations by default
                    #
                    'create_loss_and_profit': True,
                    'create_net_loss_and_profit': False,
                    'create_closing': True,
                    'create_opening': True,

                    'check_invalid_period_moves': True,
                    'check_draft_moves': True,
                    'check_unbalanced_moves': True,

                    #
                    # L&P options
                    #
                    'lp_description': _("Loss & Profit"),
                    'lp_journal_id': self._get_journal_id(
                        cr, uid, fyc, context),
                    'lp_period_id': self._get_lp_period_id(
                        cr, uid, fyc, context),
                    'lp_date': fyc.closing_fiscalyear_id.date_stop,

                    #
                    # Net L&P options
                    #
                    'nlp_description': _("Net Loss & Profit"),
                    'nlp_journal_id': self._get_journal_id(
                        cr, uid, fyc, context),
                    'nlp_period_id': self._get_lp_period_id(
                        cr, uid, fyc, context),
                    'nlp_date': fyc.closing_fiscalyear_id.date_stop,

                    #
                    # Closing options
                    #
                    'c_description': _("Fiscal Year Closing"),
                    'c_journal_id': self._get_journal_id(
                        cr, uid, fyc, context),
                    'c_period_id': self._get_c_period_id(
                        cr, uid, fyc, context),
                    'c_date': fyc.closing_fiscalyear_id.date_stop,

                    #
                    # Opening options
                    #
                    'o_description': _("Fiscal Year Opening"),
                    'o_journal_id': self._get_journal_id(
                        cr, uid, fyc, context),
                    'o_period_id': self._get_o_period_id(
                        cr, uid, fyc, context),
                    'o_date': fyc.opening_fiscalyear_id.date_start,

                    # *** New state ***
                    'state': 'draft',
                }
                self.write(cr, uid, [fyc.id], vals)
        return True

    def action_run(self, cr, uid, ids, context=None):
        """
        Called when the create entries button is used.
        """
        # Note: Just change the state,
        # everything else is done on the run wizard
        #       *before* this action is called.
        self.write(cr, uid, ids, {'state': 'in_progress'})
        return True

    def action_confirm(self, cr, uid, ids, context=None):
        """
        Called when the user clicks the confirm button.
        """
        if context is None:
            context = {}
        #
        # Make sure the lang is defined on the context
        #
        user = self.pool.get('res.users').browse(cr, uid, uid, context)
        context['lang'] = context.get('lang') or user.lang

        for fyc in self.browse(cr, uid, ids, context):
            #
            # Require the L&P, closing, and opening moves to exist
            # (NL&P is optional)
            #
            if not fyc.loss_and_profit_move_id:
                raise osv.except_osv(
                    _("Not all the operations have been performed!"),
                    _("The Loss & Profit move is required"))
            if not fyc.closing_move_id:
                raise osv.except_osv(
                    _("Not all the operations have been performed!"),
                    _("The Closing move is required"))
            if not fyc.opening_move_id:
                raise osv.except_osv(
                    _("Not all the operations have been performed!"),
                    _("The Opening move is required"))

        # Done
        self.write(cr, uid, ids, {'state': 'done'})
        return True

    def action_cancel(self, cr, uid, ids, context=None):
        """
        Called when the user clicks the cancel button.
        """
        if context is None:
            context = {}
        #
        # Make sure the lang is defined on the context
        #
        user = self.pool.get('res.users').browse(cr, uid, uid, context)
        context['lang'] = context.get('lang') or user.lang

        #
        # Uncheck all the operations
        #
        self.pool.get('account_fiscal_year_closing.fyc').write(cr, uid, ids, {
            'create_loss_and_profit': False,
            'create_net_loss_and_profit': False,
            'create_closing': False,
            'create_opening': False,
            'check_invalid_period_moves': False,
            'check_draft_moves': False,
            'check_unbalanced_moves': False,
        }, context=context)

        for fyc in self.browse(cr, uid, ids, context):
            if fyc.loss_and_profit_move_id:
                fyc.loss_and_profit_move_id.unlink()
            if fyc.net_loss_and_profit_move_id:
                fyc.net_loss_and_profit_move_id.unlink()
            if fyc.closing_move_id:
                fyc.closing_move_id.unlink()
            if fyc.opening_move_id:
                fyc.opening_move_id.unlink()

        # Canceled
        self.write(cr, uid, ids, {'state': 'canceled'})
        return True

    def action_recover(self, cr, uid, ids, context=None):
        """
        Called when the user clicks the draft button to create
        a new workflow instance.
        """
        self.write(cr, uid, ids, {'state': 'new'})
        wf_service = netsvc.LocalService("workflow")
        for item_id in ids:
            wf_service.trg_create(
                uid, 'account_fiscal_year_closing.fyc', item_id, cr)
        return True


fiscal_year_closing()
