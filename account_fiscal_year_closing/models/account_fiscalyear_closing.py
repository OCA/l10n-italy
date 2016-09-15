# -*- coding: utf-8 -*-
# Copyright 2016 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from openerp import api, fields, models, _
from openerp.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


class AccountFiscalyearClosing(models.Model):
    _name = "account.fiscalyear.closing"
    _description = "Fiscal year closing"

    def _default_fiscalyear(self):
        company = self._default_company()
        last_month_day = '%s-%s' % (
            company.fiscalyear_last_month or '12',
            company.fiscalyear_last_day or '31',
        )
        lock_date = company.fiscalyear_lock_date or fields.Date.today()
        fiscalyear = int(lock_date[:4])
        if lock_date[5:] < last_month_day:
            fiscalyear = fiscalyear - 1
        return str(fiscalyear)

    def _default_name(self):
        return self._default_fiscalyear()

    def _default_company(self):
        return self.env['res.company']._company_default_get(
            'account.fiscalyear.closing')

    def _default_date_start(self):
        date_end = fields.Date.from_string(self._default_date_end())
        return fields.Date.to_string(
            date_end - relativedelta(years=1) + relativedelta(days=1))

    def _default_date_end(self):
        company = self._default_company()
        fiscalyear = self._default_fiscalyear()
        return '%s-%s-%s' % (
            fiscalyear,
            company.fiscalyear_last_month or '12',
            company.fiscalyear_last_day or '31',
        )

    def _default_date_opening(self):
        date_end = fields.Date.from_string(self._default_date_end())
        return fields.Date.to_string(
            date_end + relativedelta(days=1))

    def _default_journal(self):
        # Used in inherited models
        return self.env['account.journal'].search([
            ('code', '=', 'MISC'),
        ], limit=1)

    def _default_move_config_ids(self):
        # To be inherited in localization modules
        return []

    name = fields.Char(
        string="Description", default=_default_name, required=True)
    company_id = fields.Many2one(
        comodel_name='res.company', string="Company", ondelete='cascade',
        readonly=True, required=True, default=_default_company)
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('calculated', 'Processed'),
        ('posted', 'Posted'),
        ('cancelled', 'Cancelled'),
    ], string="State", readonly=True, default='draft')
    calculation_date = fields.Datetime(
        string="Calculation date", readonly=True)

    date_start = fields.Date(
        string="From date", default=_default_date_start, required=True)
    date_end = fields.Date(
        string="To date", default=_default_date_end, required=True)
    date_opening = fields.Date(
        string="Opening date", default=_default_date_opening, required=True)

    check_draft_moves = fields.Boolean(
        string="Check draft moves", default=True,
        help="Checks that there are no draft moves on the fiscal year "
             "that is being closed. Non-confirmed moves won't be taken in "
             "account on the closing operations.")

    move_config_ids = fields.One2many(
        comodel_name='account.fiscalyear.closing.config',
        inverse_name='fyc_id', string="Moves configuration",
        default=_default_move_config_ids)
    move_ids = fields.One2many(
        comodel_name='account.move', inverse_name='fyc_id', string="Moves",
        readonly=True)
    move_line_ids = fields.One2many(
        comodel_name='account.move.line', inverse_name='fyc_id',
        string="Move lines", readonly=True)

    @api.model
    def _account_closing_types_get(self, types):
        types = types or {}
        account_closing_types = []
        for xmlid, closing_type in types.iteritems():
            account_type = self.env.ref(xmlid)
            if account_type:
                account_closing_types.append({
                    'account_type_id': account_type.id,
                    'closing_type': closing_type,
                })
            else:
                _logger.warning("Account type '%s' not found", xmlid)
        return account_closing_types

    @api.model
    def _account_mappings_get(self, company, mapping):
        # Generic account mappings generator, used in inherited models
        # 'mapping' is a list of 3-tuples with this format:
        #   (<source account code>, <dest account code>, <description>)
        account_mappings = []
        for src, dst, name in mapping:
            # Find the source account
            src_accounts = self.env['account.account'].search([
                ('company_id', '=', company.id),
                ('code', '=ilike', src),
            ], order="code ASC")
            dst_account = False
            if src_accounts:
                # Find the destination account
                if dst:
                    dst_account = self.env['account.account'].search([
                        ('company_id', '=', company.id),
                        ('code', '=ilike', dst),
                    ], limit=1)
                    # Use an error name if no destination account found
                    if not dst_account:
                        name = _("No destination account '%s' found for "
                                 "account '%s'") % (dst, src)
                if not name:
                    # Use first source account name if not provided
                    name = src_accounts[0].name
                data = {
                    'name': name,
                    'src_account_ids': [(6, False, src_accounts.ids)],
                }
                if dst_account:
                    data['dst_account_id'] = dst_account.id
                account_mappings.append(data)
        return account_mappings

    @api.multi
    def draft_moves_check(self):
        for closing in self:
            draft_moves = self.env['account.move'].search([
                ('company_id', '=', closing.company_id.id),
                ('state', '=', 'draft'),
                ('date', '>=', closing.date_start),
                ('date', '<=', closing.date_end),
            ])
            if draft_moves:
                msg = _('One or more draft moves found: \n')
                for move in draft_moves:
                    msg += ('ID: %s, Date: %s, Number: %s, Ref: %s\n' %
                            (move.id, move.date, move.name, move.ref))
                raise ValidationError(msg)
        return True

    @api.multi
    def calculate(self):
        for closing in self:
            # Perform checks, raise exception if check fails
            if closing.check_draft_moves:
                closing.draft_moves_check()
            # Create moves following move_config_ids
            for config in closing.move_config_ids.filtered('enable'):
                config.moves_create()
        return True

    @api.multi
    def _moves_remove(self):
        for closing in self.with_context(search_fyc_moves=True):
            closing.move_ids.button_cancel()
            closing.move_ids.unlink()
        return True

    @api.multi
    def button_calculate(self):
        res = self.with_context(search_fyc_moves=True).calculate()
        self.write({
            'state': 'calculated',
            'calculation_date': fields.Datetime.now(),
        })
        return res

    @api.multi
    def button_recalculate(self):
        self._moves_remove()
        return self.button_calculate()

    @api.multi
    def button_post(self):
        # Post moves
        for closing in self.with_context(search_fyc_moves=True):
            closing.move_ids.post()
            for config in closing.move_config_ids.filtered('reconcile'):
                config.move_id.move_reverse_reconcile()
        self.write({'state': 'posted'})
        return True

    @api.multi
    def button_open_moves(self):
        # Return an action for showing moves
        return {
            'name': _('Fiscal closing moves'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('fyc_id', 'in', self.ids)],
            'context': {'search_fyc_moves': True},
        }

    @api.multi
    def button_open_move_lines(self):
        return {
            'name': _('Fiscal closing move lines'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.move.line',
            'domain': [('fyc_id', 'in', self.ids)],
            'context': {'search_fyc_moves': True},
        }

    @api.multi
    def button_cancel(self):
        self._moves_remove()
        self.write({'state': 'cancelled'})
        return True

    @api.multi
    def button_recover(self):
        self.write({
            'state': 'draft',
            'calculation_date': False,
        })
        return True
