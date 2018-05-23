# -*- coding: utf-8 -*-
# Copyright (C) 2012 Andrea Cometa.
# Email: info@andreacometa.it
# Web site: http://www.andreacometa.it
# Copyright (C) 2012 Associazione OpenERP Italia
# (<http://www.odoo-italia.org>).
# Copyright (C) 2012-2017 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, workflow, _
from odoo.exceptions import Warning as UserError
import odoo.addons.decimal_precision as dp
from datetime import date


class RibaList(models.Model):

    @api.multi
    def _compute_acceptance_move_ids(self):
        for riba in self:
            move_ids = self.env['account.move']
            for line in riba.line_ids:
                move_ids |= line.acceptance_move_id
            riba.acceptance_move_ids = move_ids

    @api.multi
    def _compute_unsolved_move_ids(self):
        for riba in self:
            move_ids = self.env['account.move']
            for line in riba.line_ids:
                move_ids |= line.unsolved_move_id
            riba.unsolved_move_ids = move_ids

    @api.multi
    def _compute_payment_ids(self):
        for riba in self:
            move_lines = self.env['account.move.line']
            for line in riba.line_ids:
                move_lines |= line.payment_ids
            riba.payment_ids = move_lines

    _name = 'riba.distinta'
    _description = 'Riba list'

    name = fields.Char(
        'Reference', required=True, readonly=True,
        states={'draft': [('readonly', False)]},
        default=(lambda self: self.env['ir.sequence'].next_by_code(
            'riba.distinta'))
    )
    config_id = fields.Many2one(
        'riba.configuration', string='Configuration', index=True,
        required=True, readonly=True, states={'draft': [('readonly', False)]},
        help='Riba configuration to be used')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('accepted', 'Accepted'),
        ('accredited', 'Accredited'),
        ('paid', 'Paid'),
        ('unsolved', 'Unsolved'),
        ('cancel', 'Canceled')], 'State', readonly=True,
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
        compute='_compute_acceptance_move_ids',
        string="Acceptance Entries")
    accreditation_move_id = fields.Many2one(
        'account.move', 'Accreditation Entry', readonly=True)
    payment_ids = fields.Many2many(
        'account.move.line', compute='_compute_payment_ids', string='Payments')
    unsolved_move_ids = fields.Many2many(
        'account.move',
        compute='_compute_unsolved_move_ids',
        string="Unsolved Entries")
    type = fields.Selection(
        string="Type", related='config_id.type', readonly=True)
    registration_date = fields.Date(
        'Registration Date',
        states={'draft': [('readonly', False)],
                'cancel': [('readonly', False)], },
        readonly=True,
        required=True,
        default=lambda self: fields.Date.context_today(self),
        help="Keep empty to use the current date")

    @api.multi
    def unlink(self):
        for riba_list in self:
            if riba_list.state not in ('draft',  'cancel'):
                raise UserError(_(
                    'List %s is in state %s. You can only delete documents'
                    ' in state draft or canceled')
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

    @api.multi
    def settle_all_line(self):
        for riba_list in self:
            for line in riba_list.line_ids:
                if line.state == 'accredited':
                    line.riba_line_settlement()

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
    _name = 'riba.distinta.line'
    _description = 'Riba details'
    _rec_name = 'sequence'

    @api.multi
    def _compute_line_values(self):
        for line in self:
            line.amount = 0.0
            line.invoice_date = ""
            line.invoice_number = ""
            for move_line in line.move_line_ids:
                line.amount += move_line.amount
                if not line.invoice_date:
                    line.invoice_date = str(fields.Date.from_string(
                        move_line.move_line_id.invoice_id.date_invoice
                    ).strftime('%d/%m/%Y'))
                else:
                    line.invoice_date = "%s, %s" % (
                        line.invoice_date, str(fields.Date.from_string(
                            move_line.move_line_id.invoice_id.date_invoice
                        ).strftime('%d/%m/%Y')))
                if not line.invoice_number:
                    line.invoice_number = str(
                        move_line.move_line_id.invoice_id.move_name)
                else:
                    line.invoice_number = "%s, %s" % (line.invoice_number, str(
                        move_line.move_line_id.invoice_id.move_name))

    amount = fields.Float(
        compute='_compute_line_values', string="Amount")
    invoice_date = fields.Char(
        compute='_compute_line_values', string="Invoice Date", size=256)
    invoice_number = fields.Char(
        compute='_compute_line_values', string="Invoice Number", size=256)

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
    def test_reconciled(self):
        # check whether all corresponding account move lines are reconciled
        line_ids = self.move_line_id_payment_get()
        if not line_ids:
            return False
        move_lines = self.env['account.move.line'].browse(line_ids)
        reconcilied = all(line.reconciled for line in move_lines)
        return reconcilied

    @api.multi
    def _compute_lines(self):
        for riba_line in self:
            payment_lines = []
            if (
                riba_line.acceptance_move_id and not
                riba_line.state == 'unsolved'
            ):
                for line in riba_line.acceptance_move_id.line_ids:
                    payment_lines.extend(filter(None, [
                        rp.credit_move_id.id for rp in line.matched_credit_ids
                    ]))
            riba_line.payment_ids = self.env['account.move.line'].browse(
                list(set(payment_lines)))

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
        related='bank_id.acc_number', string='IBAN', store=False,
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
    ], 'State', readonly=True, track_visibility='onchange')
    payment_ids = fields.Many2many(
        'account.move.line', compute='_compute_lines', string='Payments')
    type = fields.Char(
        relation='distinta_id.type', size=32, string='Type', readonly=True)

    @api.multi
    def confirm(self):
        move_model = self.env['account.move']
        move_line_model = self.env['account.move.line']
        for line in self:
            journal = line.distinta_id.config_id.acceptance_journal_id
            total_credit = 0.0
            move = move_model.create({
                'ref': 'Ri.Ba. %s - line %s' % (line.distinta_id.name,
                                                line.sequence),
                'journal_id': journal.id,
                'date': line.distinta_id.registration_date,
            })
            to_be_reconciled = self.env['account.move.line']
            for riba_move_line in line.move_line_ids:
                total_credit += riba_move_line.amount
                move_line = move_line_model.with_context({
                    'check_move_validity': False
                }).create(
                    {
                        'name': (
                            riba_move_line.move_line_id.invoice_id and
                            riba_move_line.move_line_id.invoice_id.number or
                            riba_move_line.move_line_id.name),
                        'partner_id': line.partner_id.id,
                        'account_id': (
                            riba_move_line.move_line_id.account_id.id),
                        'credit': riba_move_line.amount,
                        'debit': 0.0,
                        'move_id': move.id,
                    }
                )
                to_be_reconciled |= move_line
                to_be_reconciled |= riba_move_line.move_line_id
            move_line_model.with_context({
                'check_move_validity': False
            }).create({
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
                'move_id': move.id,
            })
            move.post()
            to_be_reconciled.reconcile()
            line.write({
                'acceptance_move_id': move.id,
                'state': 'confirmed',
            })
            line.distinta_id.signal_workflow('accepted')

    @api.multi
    def riba_line_settlement(self):
        for riba_line in self:
            if not riba_line.distinta_id.config_id.settlement_journal_id:
                raise UserError(_('Please define a Settlement journal'))

            # trovare le move line delle scritture da chiudere
            move_model = self.env['account.move']
            move_line_model = self.env['account.move.line']

            settlement_move_line = move_line_model.search([
                ('account_id', '=', riba_line.acceptance_account_id.id),
                ('move_id', '=', riba_line.acceptance_move_id.id),
                ('debit', '!=', 0)
                ])

            settlement_move_amount = settlement_move_line.debit

            move_ref = "Settlement RIBA {} - {}".format(
                riba_line.distinta_id.name,
                riba_line.partner_id.name,
                )
            settlement_move = move_model.create({
                'journal_id':
                    riba_line.distinta_id.config_id.settlement_journal_id.id,
                'date': date.today().strftime('%Y-%m-%d'),
                'ref': move_ref,
                })

            move_line_credit = move_line_model.with_context({
                'check_move_validity': False}).create(
                {
                    'name': move_ref,
                    'partner_id': riba_line.partner_id.id,
                    'account_id':
                        riba_line.acceptance_account_id.id,
                    'credit': settlement_move_amount,
                    'debit': 0.0,
                    'move_id': settlement_move.id,
                }
            )

            accr_acc = riba_line.distinta_id.config_id.accreditation_account_id
            move_line_model.with_context({
                'check_move_validity': False}).create(
                {
                    'name': move_ref,
                    'account_id': accr_acc.id,
                    'credit': 0.0,
                    'debit': settlement_move_amount,
                    'move_id': settlement_move.id,
                }
            )

            to_be_settled = self.env['account.move.line']
            to_be_settled |= move_line_credit
            to_be_settled |= settlement_move_line

            to_be_settled.reconcile()
            settlement_move.post()


class RibaListMoveLine(models.Model):

    _name = 'riba.distinta.move.line'
    _description = 'Riba details'
    _rec_name = 'amount'

    amount = fields.Float(
        'Amount', digits=dp.get_precision('Account'))
    move_line_id = fields.Many2one(
        'account.move.line', string='Credit move line')
    riba_line_id = fields.Many2one(
        'riba.distinta.line', string='List line', ondelete='cascade')
