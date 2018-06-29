# -*- coding: utf-8 -*-
# Copyright 2015 Alessandro Camilli (<http://www.openforce.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo import netsvc


class WithholdingTax(models.Model):
    _name = 'withholding.tax'
    _description = 'Withholding Tax'

    @api.one
    @api.depends('rate_ids.date_start', 'rate_ids.date_stop', 'rate_ids.base',
                 'rate_ids.tax')
    def _get_rate(self):
        self.env.cr.execute('''
            SELECT tax, base FROM withholding_tax_rate
                WHERE withholding_tax_id = %s
                 and (date_start <= current_date or date_start is null)
                ORDER by date_start LIMIT 1''',
                            (self.id,))
        rate = self.env.cr.fetchone()
        if rate:
            self.tax = rate[0]
            self.base = rate[1]
        else:
            self.tax = 0
            self.base = 1

    def _default_wt_journal(self):
        misc_journal = self.env['account.journal'].search(
            [("code", "=", "MISC")])
        if misc_journal:
            return misc_journal[0].id
        return False

    active = fields.Boolean('Active', default=True)
    company_id = fields.Many2one(
        'res.company', string='Company', required=True, default=lambda self:
        self.env['res.company']._company_default_get('account.account'))
    name = fields.Char('Name', size=256, required=True)
    code = fields.Char('Code', size=256, required=True)
    certification = fields.Boolean('Certification')
    comment = fields.Text('Text')
    sequence = fields.Integer('Sequence')
    account_receivable_id = fields.Many2one(
        'account.account', string='Account Receivable', required=True)
    account_payable_id = fields.Many2one(
        'account.account', string='Account Payable', required=True)
    journal_id = fields.Many2one(
        'account.journal', string="Withholding tax journal",
        help="Journal used at invoice payment to register withholding tax",
        default=lambda self: self._default_wt_journal(), required=True
    )
    payment_term = fields.Many2one('account.payment.term', 'Payment Terms',
                                   required=True)
    tax = fields.Float(string='Tax %', compute='_get_rate')
    base = fields.Float(string='Base', compute='_get_rate')
    rate_ids = fields.One2many('withholding.tax.rate', 'withholding_tax_id',
                               'Rates', required=True)

    @api.one
    @api.constrains('rate_ids')
    def _check_rate_ids(self):
        if not self.rate_ids:
            raise ValidationError(
                _('Error! Rates are required'))

    def compute_tax(self, amount):
        res = {
            'base': 0,
            'tax': 0
        }
        if self.env.context.get('currency_id'):
            currency = self.env['res.currency'].browse(
                self.env.context['currency_id'])
        else:
            currency = self.env.user.company_id.currency_id
        prec = currency.decimal_places
        base = round(amount * self.base, prec)
        tax = round(base * ((self.tax or 0.0) / 100.0), prec)
        res['base'] = base
        res['tax'] = tax
        return res

    def get_grouping_key(self, invoice_tax_val):
        """
        Returns a string that will be used to group
        account.invoice.withholding.tax sharing the same properties
        """
        self.ensure_one()
        return str(invoice_tax_val['withholding_tax_id'])

    @api.one
    def get_base_from_tax(self, wt_amount):
        '''
        100 * wt_amount        1
        ---------------  *  -------
              % tax          Coeff
        '''
        dp_obj = self.env['decimal.precision']
        base = 0
        if wt_amount:
            # wt = self.browse(cr, uid, withholding_tax_id)
            base = round((100 * wt_amount / self.tax) * (1 / self.base),
                         dp_obj.precision_get('Account'))
        return base


class WithholdingTaxRate(models.Model):
    _name = 'withholding.tax.rate'
    _description = 'Withholding Tax Rates'

    @api.one
    @api.constrains('date_start', 'date_stop')
    def _check_date(self):
        if self.withholding_tax_id.active:
            where = []
            if self.date_start:
                where.append("((date_stop>='%s') or (date_stop is null))" %
                             (self.date_start,))
            if self.date_stop:
                where.append("((date_start<='%s') or (date_start is null))" %
                             (self.date_stop,))

            self.env.cr.execute(
                'SELECT id '
                'FROM withholding_tax_rate '
                'WHERE ' + ' and '.join(where) + (where and ' and ' or '') +
                'withholding_tax_id = %s '
                'AND id <> %s', (
                    self.withholding_tax_id.id,
                    self.id))
            if self.env.cr.fetchall():
                raise ValidationError(
                    _('Error! You cannot have 2 pricelist versions that \
                    overlap!'))

    withholding_tax_id = fields.Many2one('withholding.tax',
                                         string='Withholding Tax',
                                         ondelete='cascade', readonly=True)
    date_start = fields.Date(string='Date Start')
    date_stop = fields.Date(string='Date Stop')
    comment = fields.Text(string='Text')
    base = fields.Float(string='Base Coeff.', default=1)
    tax = fields.Float(string='Tax %')


class WithholdingTaxStatement(models.Model):

    '''
    The Withholding tax statement are created at the invoice validation
    '''

    _name = 'withholding.tax.statement'
    _description = 'Withholding Tax Statement'

    @api.multi
    @api.depends('move_ids.amount', 'move_ids.state',
                 'move_ids.reconcile_partial_id')
    def _compute_total(self):
        for statement in self:
            tot_wt_amount = 0
            tot_wt_amount_paid = 0
            for wt_move in statement.move_ids:
                tot_wt_amount += wt_move.amount
                if wt_move.state == 'paid':
                    tot_wt_amount_paid += wt_move.amount
            statement.amount = tot_wt_amount
            statement.amount_paid = tot_wt_amount_paid

    date = fields.Date('Date')
    move_id = fields.Many2one('account.move', 'Account move',
                              ondelete='cascade')
    invoice_id = fields.Many2one('account.invoice', 'Invoice',
                                 ondelete='cascade')
    partner_id = fields.Many2one('res.partner', 'Partner')
    withholding_tax_id = fields.Many2one('withholding.tax',
                                         string='Withholding Tax')
    company_id = fields.Many2one(
        'res.company', string='Company',
        related='withholding_tax_id.company_id')
    base = fields.Float('Base')
    tax = fields.Float('Tax')
    amount = fields.Float(
        string='WT amount applied', store=True, readonly=True,
        compute='_compute_total')
    amount_paid = fields.Float(string='WT amount paid', store=True,
                               readonly=True, compute='_compute_total')
    move_ids = fields.One2many('withholding.tax.move',
                               'statement_id', 'Moves')
    display_name = fields.Char(compute='_compute_display_name')

    def get_wt_competence(self, amount_reconcile):
        dp_obj = self.env['decimal.precision']
        amount_wt = 0
        for st in self:
            if st.invoice_id:
                domain = [
                    ('invoice_id', '=', st.invoice_id.id),
                    ('withholding_tax_id', '=', st.withholding_tax_id.id)]
                wt_inv = self.env['account.invoice.withholding.tax'].search(
                    domain, limit=1)
                if wt_inv:
                    amount_base = st.invoice_id.amount_untaxed * \
                        (amount_reconcile /
                         st.invoice_id.amount_net_pay)
                    base = round(amount_base * wt_inv.base_coeff, 5)
                    amount_wt = round(base * wt_inv.tax_coeff,
                                      dp_obj.precision_get('Account'))
            elif st.move_id:
                tax_data = st.withholding_tax_id.compute_tax(amount_reconcile)
                amount_wt = tax_data['tax']
            return amount_wt

    def _compute_display_name(self):
        self.display_name = \
            self.partner_id.name + ' - ' + self.withholding_tax_id.name


class WithholdingTaxMove(models.Model):

    '''
    The Withholding tax moves are created at the payment of invoice using
    voucher
    '''
    _name = 'withholding.tax.move'
    _description = 'Withholding Tax Move'

    state = fields.Selection([
        ('due', 'Due'),
        ('paid', 'Paid'),
    ], 'Status', readonly=True, copy=False, default='due')
    statement_id = fields.Many2one('withholding.tax.statement', 'Statement')
    date = fields.Date('Date Competence')
    reconcile_partial_id = fields.Many2one(
        'account.partial.reconcile', 'Reconcile Partial', ondelete='cascade')
    payment_line_id = fields.Many2one(
        'account.move.line', 'Payment Line', ondelete='cascade')
    credit_debit_line_id = fields.Many2one(
        'account.move.line', 'Credit/Debit Line', ondelete='cascade')
    move_line_id = fields.Many2one(
        'account.move.line', 'Account Move line',
        ondelete='cascade', help="Used from trace WT from other parts")
    withholding_tax_id = fields.Many2one('withholding.tax', 'Withholding Tax')
    company_id = fields.Many2one(
        'res.company', string='Company',
        related='withholding_tax_id.company_id')
    amount = fields.Float('Amount')
    partner_id = fields.Many2one('res.partner', 'Partner')
    date_maturity = fields.Date('Date Maturity')
    account_move_id = fields.Many2one('account.move', 'Payment Move',
                                      ondelete='cascade')
    wt_account_move_id = fields.Many2one(
        'account.move', 'WT Move', ondelete='cascade')
    display_name = fields.Char(compute='_compute_display_name')

    def unlink(self):
        for rec in self:
            if rec.state not in ['due']:
                raise ValidationError(
                    _(('Warning! You can not delete withholding tax move in\
                     state: {}').format(rec.state)))
        return super(WithholdingTaxMove, self).unlink()

    def generate_account_move(self):
        """
        Creation of account move to increase credit/debit vs tax authority
        """
        if self.wt_account_move_id:
            raise ValidationError(
                _('Warning! Wt account move already exists: %s') % (
                    self.wt_account_move_id.name))
        # Move - head
        move_vals = {
            'ref': _('WT %s - %s') % (
                self.withholding_tax_id.code,
                self.credit_debit_line_id.move_id.name),
            'journal_id': self.withholding_tax_id.journal_id.id,
            'date': self.payment_line_id.move_id.date,
        }
        # Move - lines
        move_lines = []
        for type in ('partner', 'tax'):
            ml_vals = {
                'ref': _('WT %s - %s - %s') % (
                    self.withholding_tax_id.code, self.partner_id.name,
                    self.credit_debit_line_id.move_id.name),
                'name': '%s' % (self.credit_debit_line_id.move_id.name),
                'date': move_vals['date']
            }
            # Credit/Debit line
            if type == 'partner':
                ml_vals['partner_id'] = self.payment_line_id.partner_id.id
                ml_vals['account_id'] = \
                    self.credit_debit_line_id.account_id.id
                ml_vals['withholding_tax_generated_by_move_id'] = \
                    self.payment_line_id.move_id.id
                if self.payment_line_id.credit:
                    ml_vals['credit'] = self.amount
                else:
                    ml_vals['debit'] = self.amount
            # Authority tax line
            elif type == 'tax':
                ml_vals['name'] = '%s - %s' % (
                    self.withholding_tax_id.code,
                    self.credit_debit_line_id.move_id.name)
                if self.payment_line_id.credit:
                    ml_vals['debit'] = self.amount
                    ml_vals['account_id'] = \
                        self.withholding_tax_id.account_payable_id.id
                else:
                    ml_vals['credit'] = self.amount
                    ml_vals['account_id'] = \
                        self.withholding_tax_id.account_receivable_id.id
            # self.env['account.move.line'].create(move_vals)
            move_lines.append((0, 0, ml_vals))

        move_vals['line_ids'] = move_lines
        move = self.env['account.move'].create(move_vals)
        move.post()
        # Save move in the wt move
        self.wt_account_move_id = move.id

        # Find lines for reconcile
        line_to_reconcile = False
        for line in move.line_ids:
            if line.account_id.user_type_id.type in ['payable', 'receivable']:
                line_to_reconcile = line
                break
        if line_to_reconcile:
            self.env['account.partial.reconcile'].\
                with_context(no_generate_wt_move=True).create({
                    'debit_move_id': line_to_reconcile.id,
                    'credit_move_id': self.credit_debit_line_id.id,
                    'amount': self.amount,
                })

    def _compute_display_name(self):
        self.display_name = \
            self.partner_id.name + ' - ' + self.withholding_tax_id.name

    @api.multi
    def action_paid(self):
        for pt in self:
            wf_service = netsvc.LocalService("workflow")
            wf_service.trg_validate(self.env.uid, self._name, pt.id, 'paid',
                                    self.env.cr)

    @api.multi
    def action_set_to_draft(self):
        for pt in self:
            wf_service = netsvc.LocalService("workflow")
            wf_service.trg_validate(self.env.uid, self._name, pt.id, 'cancel',
                                    self.env.cr)

    @api.multi
    def move_paid(self):
        for move in self:
            if move.state in ['due']:
                move.write({'state': 'paid'})

    @api.multi
    def move_set_due(self):
        for move in self:
            if move.state in ['paid']:
                move.write({'state': 'due'})

    @api.multi
    def check_unlink(self):
        wt_moves_not_eresable = []
        for move in self:
            if move.state not in ['due']:
                wt_moves_not_eresable.append(move)
        if wt_moves_not_eresable:
            raise ValidationError(
                _('Warning! Only Withholding Tax moves in Due status \
                    can be deleted'))
