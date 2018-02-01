# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2012 Andrea Cometa.
#    Email: info@andreacometa.it
#    Web site: http://www.andreacometa.it
#    Copyright (C) 2012-2015 Lorenzo Battistini - Agile Business Group
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    Copyright (C) 2014 Associazione Odoo Italia
#    (<http://www.odoo-italia.org>).
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
##############################################################################

from openerp import fields, models, api, workflow, _
from openerp.exceptions import Warning as UserError
import openerp.addons.decimal_precision as dp


class RibaList(models.Model):

    @api.one
    def _get_acceptance_move_ids(self):
        move_ids = self.env['account.move']
        for line in self.line_ids:
            move_ids |= line.acceptance_move_id
        self.acceptance_move_ids = move_ids

    @api.one
    def _get_unsolved_move_ids(self):
        move_ids = self.env['account.move']
        for line in self.line_ids:
            move_ids |= line.unsolved_move_id
        self.unsolved_move_ids = move_ids

    @api.one
    def _get_payment_ids(self):
        move_lines = self.env['account.move.line']
        for line in self.line_ids:
            move_lines |= line.payment_ids
        self.payment_ids = move_lines

    _name = 'riba.distinta'
    _description = 'Riba list'

    name = fields.Char(
        'Reference', required=True, readonly=True,
        states={'draft': [('readonly', False)]},
        default=(lambda self: self.env['ir.sequence'].get('riba.distinta')))
    config_id = fields.Many2one(
        'riba.configuration', string='Configuration', select=True,
        required=True, readonly=True, states={'draft': [('readonly', False)]},
        help='Riba configuration to be used')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('accepted', 'Accepted'),
        ('accredited', 'Accredited'),
        ('paid', 'Paid'),
        ('unsolved', 'Unsolved'),
        ('cancel', 'Canceled')], 'State', select=True, readonly=True,
        default='draft')
    line_ids = fields.One2many(
        'riba.distinta.line', 'distinta_id', 'Riba deadlines', readonly=True,
        states={'draft': [('readonly', False)]})
    user_id = fields.Many2one(
        'res.users', 'User', required=True, readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env.user,)
    date_created = fields.Date(
        'Creation date', readonly=True,
        default=lambda self: fields.Date.context_today(self))
    date_accepted = fields.Date('Acceptance date')
    date_accreditation = fields.Date('Accreditation date')
    date_paid = fields.Date('Paid date', readonly=True)
    date_unsolved = fields.Date('Unsolved date', readonly=True)
    company_id = fields.Many2one(
        'res.company', 'Company', required=True, readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env['res.company']._company_default_get(
            'riba.distinta'))
    acceptance_move_ids = fields.Many2many(
        'account.move',
        compute='_get_acceptance_move_ids',
        string="Acceptance Entries")
    accreditation_move_id = fields.Many2one(
        'account.move', 'Accreditation Entry', readonly=True)
    payment_ids = fields.Many2many(
        'account.move.line', compute='_get_payment_ids', string='Payments')
    unsolved_move_ids = fields.Many2many(
        'account.move',
        compute='_get_unsolved_move_ids',
        string="Unsolved Entries")
    type = fields.Selection(
        string="Type", related='config_id.type', readonly=True)
    registration_date = fields.Date(
        'Registration Date',
        states={'draft': [('readonly', False)],
                'cancel': [('readonly', False)], },
        select=True, readonly=True,
        required=True,
        default=lambda self: fields.Date.context_today(self),
        help="Keep empty to use the current date")

    @api.multi
    def unlink(self):
        for riba_list in self:
            if riba_list.state not in ('draft',  'cancel'):
                raise UserError(
                    'List %s is in state %s. You can only delete documents'
                    ' in state draft or canceled'
                    % (riba_list.name, riba_list.state))
        super(RibaList, self).unlink()

    @api.multi
    def confirm(self):
        for list in self:
            for line in list.line_ids:
                line.confirm()

    @api.multi
    def riba_new(self):
        self.state = 'draft'

    @api.multi
    def riba_cancel(self):
        for riba_list in self:
            for line in riba_list.line_ids:
                line.state = 'cancel'
                if line.acceptance_move_id:
                    line.acceptance_move_id.unlink()
                if line.unsolved_move_id:
                    line.unsolved_move_id.unlink()
            if riba_list.accreditation_move_id:
                riba_list.accreditation_move_id.unlink()
            riba_list.state = 'cancel'

    @api.onchange('date_accepted', 'date_accreditation')
    def _onchange_date(self):
        if self.date_accepted and self.date_accreditation:
            if self.date_accepted > self.date_accreditation:
                raise UserError(_(
                    "Date accreditation must be greater or equal to"
                    " date acceptance"))

    @api.multi
    def riba_accepted(self):
        self.state = 'accepted'
        if not self.date_accepted:
            self.date_accepted = fields.Date.context_today(self)

    @api.multi
    def riba_accredited(self):
        self.state = 'accredited'
        if not self.date_accreditation:
            self.date_accreditation = fields.Date.context_today(self)
        for riba_list in self:
            for line in riba_list.line_ids:
                line.state = 'accredited'

    @api.multi
    def riba_paid(self):
        self.state = 'paid'
        self.date_paid = fields.Date.context_today(self)

    @api.multi
    def riba_unsolved(self):
        self.state = 'unsolved'
        self.date_unsolved = fields.Date.context_today(self)

    @api.multi
    def test_state(self, state):
        for riba_list in self:
            for line in riba_list.line_ids:
                if line.state != state:
                    return False
        return True

    @api.multi
    def test_accepted(self):
        return self.test_state('confirmed')

    @api.multi
    def test_unsolved(self):
        return self.test_state('unsolved')

    @api.multi
    def test_paid(self):
        return self.test_state('paid')

    @api.multi
    def action_cancel_draft(self):
        for riba_list in self:
            workflow.trg_delete(
                self.env.user.id, 'riba.distinta', riba_list.id, self._cr)
            workflow.trg_create(
                self.env.user.id, 'riba.distinta', riba_list.id, self._cr)
            riba_list.state = 'draft'
            for line in riba_list.line_ids:
                line.state = 'draft'


class RibaListLine(models.Model):
    # TODO estendere la account_due_list per visualizzare e filtrare
    # in base alle riba ?
    _name = 'riba.distinta.line'
    _description = 'Riba details'
    _rec_name = 'sequence'

    @api.one
    def _get_line_values(self):
        self.amount = 0.0
        self.invoice_date = ""
        self.invoice_number = ""
        for move_line in self.move_line_ids:
            self.amount += move_line.amount
            if not self.invoice_date:
                self.invoice_date = str(fields.Date.from_string(
                    move_line.move_line_id.invoice.date_invoice
                ).strftime('%d/%m/%Y'))
            else:
                self.invoice_date = "%s, %s" % (
                    self.invoice_date, str(fields.Date.from_string(
                        move_line.move_line_id.invoice.date_invoice
                    ).strftime('%d/%m/%Y')))
            if not self.invoice_number:
                self.invoice_number = str(
                    move_line.move_line_id.invoice.internal_number)
            else:
                self.invoice_number = "%s, %s" % (self.invoice_number, str(
                    move_line.move_line_id.invoice.internal_number))

    amount = fields.Float(
        compute='_get_line_values', string="Amount")
    invoice_date = fields.Char(
        compute='_get_line_values', string="Invoice Date", size=256)
    invoice_number = fields.Char(
        compute='_get_line_values', string="Invoice Number", size=256)

    @api.multi
    def move_line_id_payment_get(self):
        # return the move line ids with the same account as the distinta line
        if not self.id:
            return []
        query = """ SELECT l.id
                    FROM account_move_line l, riba_distinta_line rdl
                    WHERE rdl.id = %s AND l.move_id = rdl.acceptance_move_id
                    AND l.account_id = rdl.acceptance_account_id
                """
        self._cr.execute(query, (self.id,))
        return [row[0] for row in self._cr.fetchall()]

    @api.multi
    def test_reconcilied(self):
        # check whether all corresponding account move lines are reconciled
        line_ids = self.move_line_id_payment_get()
        if not line_ids:
            return False
        query = "SELECT reconcile_id FROM account_move_line WHERE id IN %s"
        self._cr.execute(query, (tuple(line_ids),))
        reconcilied = all(row[0] for row in self._cr.fetchall())
        return reconcilied

    @api.multi
    def _compute_lines(self):
        for line in self:
            src = []
            lines = []
            if line.acceptance_move_id and not line.state == 'unsolved':
                for m in line.acceptance_move_id.line_id:
                    temp_lines = []
                    if m.reconcile_id and m.credit == 0.0:
                        temp_lines = map(
                            lambda x: x.id, m.reconcile_id.line_id)
                    elif m.reconcile_partial_id and m.credit == 0.0:
                        temp_lines = map(
                            lambda x: x.id,
                            m.reconcile_partial_id.line_partial_ids)
                    lines += [x for x in temp_lines if x not in lines]
                    src.append(m.id)

            lines = filter(lambda x: x not in src, lines)
            line.payment_ids = self.env['account.move.line'].browse(lines)

    sequence = fields.Integer('Number')
    move_line_ids = fields.One2many(
        'riba.distinta.move.line', 'riba_line_id', string='Credit move lines')
    acceptance_move_id = fields.Many2one(
        'account.move', string='Acceptance Entry', readonly=True)
    unsolved_move_id = fields.Many2one(
        'account.move', string='Unsolved Entry', readonly=True)
    acceptance_account_id = fields.Many2one(
        'account.account', string='Acceptance Account')
    bank_id = fields.Many2one('res.partner.bank', string='Debitor Bank')
    iban = fields.Char(
        related='bank_id.iban', string='IBAN', store=False,
        readonly=True)
    distinta_id = fields.Many2one(
        'riba.distinta', string='List', required=True, ondelete='cascade')
    partner_id = fields.Many2one(
        'res.partner', string="Cliente", readonly=True)
    due_date = fields.Date("Due date", readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('accredited', 'Accredited'),
        ('paid', 'Paid'),
        ('unsolved', 'Unsolved'),
        ('cancel', 'Canceled'),
    ], 'State', select=True, readonly=True, track_visibility='onchange')
    payment_ids = fields.Many2many(
        'account.move.line', compute='_compute_lines', string='Payments')
    type = fields.Selection(
        string="Type", related='distinta_id.config_id.type', readonly=True)
    config_id = fields.Many2one(
        string="Configuration", related='distinta_id.config_id',
        readonly=True, store=True)

    @api.multi
    def confirm(self):
        move_pool = self.pool['account.move']
        move_line_pool = self.pool['account.move.line']
        for line in self:
            journal = line.distinta_id.config_id.acceptance_journal_id
            total_credit = 0.0
            period_id = self.pool['account.period'].find(
                self._cr, self.env.user.id,
                line.distinta_id.registration_date)
            move_id = move_pool.create(self._cr, self.env.user.id, {
                'ref': 'Ri.Ba. %s - line %s' % (line.distinta_id.name,
                                                line.sequence),
                'journal_id': journal.id,
                'date': line.distinta_id.registration_date,
                'period_id': period_id and period_id[0] or False,
            }, self._context)
            to_be_reconciled = []
            for riba_move_line in line.move_line_ids:
                total_credit += riba_move_line.amount
                move_line_id = move_line_pool.create(
                    self._cr, self.env.user.id, {
                        'name': (
                            riba_move_line.move_line_id.invoice and
                            riba_move_line.move_line_id.invoice.number or
                            riba_move_line.move_line_id.name),
                        'partner_id': line.partner_id.id,
                        'account_id': (
                            riba_move_line.move_line_id.account_id.id),
                        'credit': riba_move_line.amount,
                        'debit': 0.0,
                        'move_id': move_id,
                    }, self._context)
                to_be_reconciled.append([move_line_id,
                                         riba_move_line.move_line_id.id])
            move_line_pool.create(self._cr, self.env.user.id, {
                'name': 'Ri.Ba. %s - line %s' % (line.distinta_id.name,
                                                 line.sequence),
                'account_id': (
                    line.acceptance_account_id.id or
                    line.distinta_id.config_id.acceptance_account_id.id
                    # in questo modo se la riga non ha conto accettazione
                    # viene prelevato il conto in configuration riba
                ),
                'partner_id': line.partner_id.id,
                'date_maturity': line.due_date,
                'credit': 0.0,
                'debit': total_credit,
                'move_id': move_id,
            }, self._context)
            move_pool.post(
                self._cr, self.env.user.id, [move_id], self._context)
            for reconcile_ids in to_be_reconciled:
                move_line_pool.reconcile_partial(self._cr, self.env.user.id,
                                                 reconcile_ids,
                                                 self._context)
            line.write({
                'acceptance_move_id': move_id,
                'state': 'confirmed',
            })
            line.distinta_id.signal_workflow('accepted')


class RibaListMoveLine(models.Model):

    _name = 'riba.distinta.move.line'
    _description = 'Riba details'
    _rec_name = 'amount'

    amount = fields.Float(
        'Amount', digits_compute=dp.get_precision('Account'))
    move_line_id = fields.Many2one(
        'account.move.line', string='Credit move line')
    riba_line_id = fields.Many2one(
        'riba.distinta.line', string='List line', ondelete='cascade')
