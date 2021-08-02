# Copyright 2011-2012 Domsense s.r.l. (<http://www.domsense.com>).
# Copyright 2012-15 Agile Business Group sagl (<http://www.agilebg.com>)
# Copyright 2015 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import math
from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp
from odoo.tools import float_is_zero


class AccountVatPeriodEndStatement(models.Model):

    @api.multi
    def _compute_authority_vat_amount(self):
        for statement in self:
            debit_vat_amount = 0.0
            credit_vat_amount = 0.0
            generic_vat_amount = 0.0
            for debit_line in statement.debit_vat_account_line_ids:
                debit_vat_amount += debit_line.amount
            for credit_line in statement.credit_vat_account_line_ids:
                credit_vat_amount += credit_line.amount
            for generic_line in statement.generic_vat_account_line_ids:
                generic_vat_amount += generic_line.amount
            authority_amount = (
                debit_vat_amount - credit_vat_amount - generic_vat_amount -
                statement.previous_credit_vat_amount +
                statement.previous_debit_vat_amount -
                statement.tax_credit_amount +
                statement.interests_debit_vat_amount -
                statement.advance_amount
            )
            statement.authority_vat_amount = authority_amount

    @api.multi
    def _compute_deductible_vat_amount(self):
        for statement in self:
            credit_vat_amount = 0.0
            for credit_line in statement.credit_vat_account_line_ids:
                credit_vat_amount += credit_line.amount
            statement.deductible_vat_amount = credit_vat_amount

    @api.multi
    @api.depends(
        'state',
        'move_id.line_ids.amount_residual',
        'move_id.line_ids.currency_id')
    def _compute_residual(self):
        precision = self.env.user.company_id.currency_id.decimal_places
        for statement in self:
            if not statement.move_id.exists():
                statement.residual = 0.0
                statement.reconciled = False
                continue

            residual = 0.0
            for line in statement.move_id.line_ids:
                authority_vat_account_id = (
                    statement.authority_vat_account_id.id)
                if line.account_id.id == authority_vat_account_id:
                    residual += line.amount_residual
            statement.residual = abs(residual)
            if float_is_zero(statement.residual, precision_digits=precision):
                statement.reconciled = True
            else:
                statement.reconciled = False

    @api.depends('move_id.line_ids.amount_residual')
    @api.multi
    def _compute_lines(self):
        for statement in self:
            payment_lines = []
            if statement.move_id.exists():
                for line in statement.move_id.line_ids:
                    payment_lines.extend([_f for _f in [
                        rp.credit_move_id.id for rp in line.matched_credit_ids
                    ] if _f])
                    payment_lines.extend([_f for _f in [
                        rp.debit_move_id.id for rp in line.matched_debit_ids
                    ] if _f])
            statement.payment_ids = self.env['account.move.line'].browse(
                list(set(payment_lines)))

    @api.model
    def _get_default_interest(self):
        company = self.env.user.company_id
        return company.of_account_end_vat_statement_interest

    @api.model
    def _get_default_interest_percent(self):
        company = self.env.user.company_id
        if not company.of_account_end_vat_statement_interest:
            return 0
        return company.of_account_end_vat_statement_interest_percent

    _name = "account.vat.period.end.statement"
    _description = "VAT period end statement"
    _rec_name = 'date'

    debit_vat_account_line_ids = fields.One2many(
        'statement.debit.account.line', 'statement_id', 'Debit VAT',
        help='The accounts containing the debit VAT amount to write-off',
        readonly=True
    )
    credit_vat_account_line_ids = fields.One2many(
        'statement.credit.account.line', 'statement_id', 'Credit VAT',
        help='The accounts containing the credit VAT amount to write-off',
        readonly=True)
    previous_credit_vat_account_id = fields.Many2one(
        'account.account', 'Previous Credits VAT',
        help='Credit VAT from previous periods',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)]
        })
    previous_credit_vat_amount = fields.Float(
        'Previous Credits VAT Amount',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)]
        }, digits=dp.get_precision('Account'))
    previous_year_credit = fields.Boolean("Previous year credits")
    previous_debit_vat_account_id = fields.Many2one(
        'account.account', 'Previous Debits VAT',
        help='Debit VAT from previous periods',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)]
        })
    previous_debit_vat_amount = fields.Float(
        'Previous Debits VAT Amount',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)]
        }, digits=dp.get_precision('Account'))
    interests_debit_vat_account_id = fields.Many2one(
        'account.account', 'Due interests',
        help='Due interests for three-monthly statments',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)]
        })
    interests_debit_vat_amount = fields.Float(
        'Due interests Amount',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)]
        }, digits=dp.get_precision('Account'))
    tax_credit_account_id = fields.Many2one(
        'account.account', 'Tax credits',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)]
        })
    tax_credit_amount = fields.Float(
        'Tax credits Amount',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)]
        }, digits=dp.get_precision('Account'))
    advance_account_id = fields.Many2one(
        'account.account', 'Down payment',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)]
        })
    advance_amount = fields.Float(
        'Down payment Amount',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)]
        }, digits=dp.get_precision('Account'))
    advance_computation_method = fields.Selection([
        ('1', 'Storico'),
        ('2', 'Previsionale'),
        ('3', 'Analitico - effettivo'),
        ('4', '"4" (soggetti particolari)'),
    ],
        string="Down payment computation method",
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)]
        })
    generic_vat_account_line_ids = fields.One2many(
        'statement.generic.account.line', 'statement_id',
        'Other VAT Credits / Debits or Tax Compensations',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)]})
    authority_partner_id = fields.Many2one(
        'res.partner', 'Tax Authority Partner',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)]})
    authority_vat_account_id = fields.Many2one(
        'account.account', 'Tax Authority VAT Account',
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)]})
    authority_vat_amount = fields.Float(
        'Authority VAT Amount', compute="_compute_authority_vat_amount",
        digits=dp.get_precision('Account'))
    # TODO is this field needed?
    deductible_vat_amount = fields.Float(
        'Deductible VAT Amount', compute="_compute_deductible_vat_amount",
        digits=dp.get_precision('Account'))
    journal_id = fields.Many2one(
        'account.journal', 'Journal', required=True,
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)]})
    date = fields.Date(
        'Date', required=True,
        states={
            'confirmed': [('readonly', True)],
            'paid': [('readonly', True)],
            'draft': [('readonly', False)]},
        default=fields.Date.context_today)
    move_id = fields.Many2one(
        'account.move', 'VAT statement move', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
    ], 'State', readonly=True, default='draft')
    payment_term_id = fields.Many2one(
        'account.payment.term', 'Payment Term',
        states={
            'confirmed': [
                ('readonly', True)], 'paid': [('readonly', True)],
            'draft': [('readonly', False)]})
    reconciled = fields.Boolean(
        'Paid/Reconciled', compute="_compute_residual",
        help="It indicates that the statement has been paid and the "
             "journal entry of the statement has been reconciled with "
             "one or several journal entries of payment.",
        store=True, readonly=True
    )
    residual = fields.Float(
        string='Amount Due',
        compute='_compute_residual', store=True, help="Remaining amount due.",
        digits=dp.get_precision('Account'))
    payment_ids = fields.Many2many(
        'account.move.line', string='Payments', compute="_compute_lines",
        store=True)
    date_range_ids = fields.One2many(
        'date.range', 'vat_statement_id', 'Periods')
    interest = fields.Boolean(
        'Compute Interest', default=_get_default_interest)
    interest_percent = fields.Float(
        'Interest - Percent', default=_get_default_interest_percent)
    fiscal_page_base = fields.Integer(
        'Last printed page', required=True, default=0)
    fiscal_year = fields.Char(
        'Fiscal year for report')
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env['res.company']._company_default_get(
            'account.invoice'))
    annual = fields.Boolean("Annual prospect")
    account_ids = fields.Many2many('account.account', string='Accounts filter',
                                   domain=lambda self: self._get_domain_account())

    def _get_domain_account(self):
        domain = [('vat_statement_account_id', '!=', False)]
        tax_ids = self.env['account.tax'].search(domain)
        account_ids = tax_ids.mapped('vat_statement_account_id')
        return [('id', 'in', account_ids.ids)]

    @api.multi
    def unlink(self):
        for statement in self:
            if statement.state == 'confirmed' or statement.state == 'paid':
                raise UserError(
                    _('You cannot delete a confirmed or paid statement'))
        res = super(AccountVatPeriodEndStatement, self).unlink()
        return res

    @api.multi
    def set_fiscal_year(self):
        for statement in self:
            if statement.date_range_ids:
                date = min([x.date_start for x in statement.date_range_ids])
                statement.update({'fiscal_year': date.year})

    @api.multi
    def _write(self, vals):
        pre_not_reconciled = self.filtered(
            lambda statement: not statement.reconciled)
        pre_reconciled = self - pre_not_reconciled
        res = super(AccountVatPeriodEndStatement, self)._write(vals)
        reconciled = self.filtered(lambda statement: statement.reconciled)
        not_reconciled = self - reconciled
        (reconciled & pre_reconciled).filtered(
            lambda statement: statement.state == 'confirmed'
        ).statement_paid()
        (not_reconciled & pre_not_reconciled).filtered(
            lambda statement: statement.state == 'paid'
        ).statement_confirmed()
        return res

    @api.multi
    def statement_draft(self):
        for statement in self:
            if statement.move_id:
                statement.move_id.button_cancel()
                statement.move_id.unlink()
            statement.state = 'draft'

    @api.multi
    def statement_paid(self):
        for statement in self:
            statement.state = 'paid'

    @api.multi
    def statement_confirmed(self):
        for statement in self:
            statement.state = 'confirmed'

    @api.multi
    def create_move(self):
        move_obj = self.env['account.move']
        for statement in self:
            statement_date = fields.Date.to_string(statement.date)
            move_data = {
                'name': _('VAT statement') + ' - ' + statement_date,
                'date': statement_date,
                'journal_id': statement.journal_id.id,
            }
            move = move_obj.create(move_data)
            move_id = move.id
            statement.write({'move_id': move_id})
            lines_to_create = []

            for debit_line in statement.debit_vat_account_line_ids:
                if debit_line.amount != 0.0:
                    debit_vat_data = {
                        'name': _('Debit VAT'),
                        'account_id': debit_line.account_id.id,
                        'move_id': move_id,
                        'journal_id': statement.journal_id.id,
                        'debit': 0.0,
                        'credit': 0.0,
                        'date': statement_date,
                        'company_id': statement.company_id.id,
                    }

                    if debit_line.amount > 0:
                        debit_vat_data['debit'] = math.fabs(debit_line.amount)
                    else:
                        debit_vat_data['credit'] = math.fabs(debit_line.amount)
                    lines_to_create.append((0, 0, debit_vat_data))

            for credit_line in statement.credit_vat_account_line_ids:
                if credit_line.amount != 0.0:
                    credit_vat_data = {
                        'name': _('Credit VAT'),
                        'account_id': credit_line.account_id.id,
                        'move_id': move_id,
                        'journal_id': statement.journal_id.id,
                        'debit': 0.0,
                        'credit': 0.0,
                        'date': statement_date,
                        'company_id': statement.company_id.id,
                    }
                    if credit_line.amount < 0:
                        credit_vat_data['debit'] = math.fabs(
                            credit_line.amount)
                    else:
                        credit_vat_data['credit'] = math.fabs(
                            credit_line.amount)
                    lines_to_create.append((0, 0, credit_vat_data))

            if statement.previous_credit_vat_amount:
                previous_credit_vat_data = {
                    'name': _('Previous Credits VAT'),
                    'account_id': statement.previous_credit_vat_account_id.id,
                    'move_id': move_id,
                    'journal_id': statement.journal_id.id,
                    'debit': 0.0,
                    'credit': 0.0,
                    'date': statement_date,
                    'company_id': statement.company_id.id,
                }
                if statement.previous_credit_vat_amount < 0:
                    previous_credit_vat_data['debit'] = math.fabs(
                        statement.previous_credit_vat_amount)
                else:
                    previous_credit_vat_data['credit'] = math.fabs(
                        statement.previous_credit_vat_amount)
                lines_to_create.append((0, 0, previous_credit_vat_data))

            if statement.tax_credit_amount:
                tax_credit_vat_data = {
                    'name': _('Tax Credits'),
                    'account_id': statement.tax_credit_account_id.id,
                    'move_id': move_id,
                    'journal_id': statement.journal_id.id,
                    'debit': 0.0,
                    'credit': 0.0,
                    'date': statement_date,
                    'company_id': statement.company_id.id,
                }
                if statement.tax_credit_amount < 0:
                    tax_credit_vat_data['debit'] = math.fabs(
                        statement.tax_credit_amount)
                else:
                    tax_credit_vat_data['credit'] = math.fabs(
                        statement.tax_credit_amount)
                lines_to_create.append((0, 0, tax_credit_vat_data))

            if statement.advance_amount:
                advance_vat_data = {
                    'name': _('Tax Credits'),
                    'account_id': statement.advance_account_id.id,
                    'move_id': move_id,
                    'journal_id': statement.journal_id.id,
                    'debit': 0.0,
                    'credit': 0.0,
                    'date': statement_date,
                    'company_id': statement.company_id.id,
                }
                if statement.advance_amount < 0:
                    advance_vat_data['debit'] = math.fabs(
                        statement.advance_amount)
                else:
                    advance_vat_data['credit'] = math.fabs(
                        statement.advance_amount)
                lines_to_create.append((0, 0, advance_vat_data))

            if statement.previous_debit_vat_amount:
                previous_debit_vat_data = {
                    'name': _('Previous Debits VAT'),
                    'account_id': statement.previous_debit_vat_account_id.id,
                    'move_id': move_id,
                    'journal_id': statement.journal_id.id,
                    'debit': 0.0,
                    'credit': 0.0,
                    'date': statement_date,
                    'company_id': statement.company_id.id,
                }
                if statement.previous_debit_vat_amount > 0:
                    previous_debit_vat_data['debit'] = math.fabs(
                        statement.previous_debit_vat_amount)
                else:
                    previous_debit_vat_data['credit'] = math.fabs(
                        statement.previous_debit_vat_amount)
                lines_to_create.append((0, 0, previous_debit_vat_data))

            if statement.interests_debit_vat_amount:
                interests_data = {
                    'name': _('Due interests'),
                    'account_id': statement.interests_debit_vat_account_id.id,
                    'move_id': move_id,
                    'journal_id': statement.journal_id.id,
                    'debit': 0.0,
                    'credit': 0.0,
                    'date': statement_date,
                    'company_id': statement.company_id.id,
                }
                if statement.interests_debit_vat_amount > 0:
                    interests_data['debit'] = math.fabs(
                        statement.interests_debit_vat_amount)
                else:
                    interests_data['credit'] = math.fabs(
                        statement.interests_debit_vat_amount)
                lines_to_create.append((0, 0, interests_data))

            for generic_line in statement.generic_vat_account_line_ids:
                generic_vat_data = {
                    'name': _('Other VAT Credits / Debits'),
                    'account_id': generic_line.account_id.id,
                    'move_id': move_id,
                    'journal_id': statement.journal_id.id,
                    'debit': 0.0,
                    'credit': 0.0,
                    'date': statement_date,
                    'company_id': statement.company_id.id,
                }
                if generic_line.amount < 0:
                    generic_vat_data['debit'] = math.fabs(generic_line.amount)
                else:
                    generic_vat_data['credit'] = math.fabs(generic_line.amount)
                lines_to_create.append((0, 0, generic_vat_data))

            end_debit_vat_data = {
                'name': _('Tax Authority VAT'),
                'account_id': statement.authority_vat_account_id.id,
                'partner_id': statement.authority_partner_id.id,
                'move_id': move_id,
                'journal_id': statement.journal_id.id,
                'date': statement_date,
                'company_id': statement.company_id.id,
            }
            if statement.authority_vat_amount > 0:
                end_debit_vat_data['debit'] = 0.0
                end_debit_vat_data['credit'] = math.fabs(
                    statement.authority_vat_amount)
                if statement.payment_term_id:
                    due_list = statement.payment_term_id.compute(
                        statement.authority_vat_amount, statement_date)[0]
                    for term in due_list:
                        current_line = end_debit_vat_data
                        current_line['credit'] = term[1]
                        current_line['date_maturity'] = term[0]
                        lines_to_create.append((0, 0, current_line))
                else:
                    lines_to_create.append((0, 0, end_debit_vat_data))
            elif statement.authority_vat_amount < 0:
                end_debit_vat_data['debit'] = math.fabs(
                    statement.authority_vat_amount)
                end_debit_vat_data['credit'] = 0.0
                lines_to_create.append((0, 0, end_debit_vat_data))

            move.line_ids = lines_to_create
            move.post()
            statement.state = 'confirmed'

        return True

    @api.multi
    def compute_amounts(self):
        decimal_precision_obj = self.env['decimal.precision']
        debit_line_model = self.env['statement.debit.account.line']
        credit_line_model = self.env['statement.credit.account.line']
        for statement in self:
            statement.previous_debit_vat_amount = 0.0
            prev_statements = self.search(
                [('date', '<', statement.date), ('annual', '=', False)],
                order='date desc')
            if prev_statements and not statement.annual:
                prev_statement = prev_statements[0]
                if (
                    prev_statement.residual > 0 and
                    prev_statement.authority_vat_amount > 0
                ):
                    statement.write(
                        {'previous_debit_vat_amount': prev_statement.residual})
                elif prev_statement.authority_vat_amount < 0:
                    statement.write(
                        {'previous_credit_vat_amount': (
                            - prev_statement.authority_vat_amount)})
                    company = statement.company_id or self.env.user.company_id
                    statement_fiscal_year_dates = (
                        company.compute_fiscalyear_dates(
                            statement.date_range_ids and
                            statement.date_range_ids[0].date_start or
                            statement.date))
                    prev_statement_fiscal_year_dates = (
                        company.compute_fiscalyear_dates(
                            prev_statement.date_range_ids and
                            prev_statement.date_range_ids[0].date_start or
                            prev_statement.date))
                    if (
                        prev_statement_fiscal_year_dates['date_to'] <
                        statement_fiscal_year_dates['date_from']
                    ):
                        statement.write({
                            'previous_year_credit': True})

            credit_line_ids, debit_line_ids = self._get_credit_debit_lines(
                statement)

            for debit_line in statement.debit_vat_account_line_ids:
                debit_line.unlink()
            for credit_line in statement.credit_vat_account_line_ids:
                credit_line.unlink()
            for debit_vals in debit_line_ids:
                debit_vals.update({'statement_id': statement.id})
                debit_line_model.create(debit_vals)
            for credit_vals in credit_line_ids:
                credit_vals.update({'statement_id': statement.id})
                credit_line_model.create(credit_vals)

            interest_amount = 0.0
            # if exits Delete line with interest
            acc_id = self.get_account_interest().id
            statement.interests_debit_vat_account_id = None
            statement.interests_debit_vat_amount = interest_amount

            # Compute interest
            if statement.interest and statement.authority_vat_amount > 0:
                interest_amount = round(
                    statement.authority_vat_amount *
                    (float(statement.interest_percent) / 100),
                    decimal_precision_obj.precision_get('Account'))
            # Add line with interest
            if interest_amount:
                statement.interests_debit_vat_account_id = acc_id
                statement.interests_debit_vat_amount = interest_amount
        return True

    def _set_debit_lines(self, debit_tax, debit_line_ids, statement):
        total = 0.0
        for period in statement.date_range_ids:
            total += debit_tax._compute_totals_tax({
                'from_date': period.date_start,
                'to_date': period.date_end,
                'registry_type': 'customer',
            })[3]  # position 3 is deductible part
        debit_line_ids.append({
            'account_id': debit_tax.vat_statement_account_id.id,
            'tax_id': debit_tax.id,
            'amount': total,
        })

    def _set_credit_lines(self, credit_tax, credit_line_ids, statement):
        total = 0.0
        for period in statement.date_range_ids:
            total += credit_tax._compute_totals_tax({
                'from_date': period.date_start,
                'to_date': period.date_end,
                'registry_type': 'supplier',
            })[3]  # position 3 is deductible part
        credit_line_ids.append({
            'account_id': credit_tax.vat_statement_account_id.id,
            'tax_id': credit_tax.id,
            'amount': total,
        })

    def _get_credit_debit_lines(self, statement):
        credit_line_ids = []
        debit_line_ids = []
        tax_model = self.env['account.tax']
        taxes = tax_model.search([
            ('vat_statement_account_id', '!=', False),
            ('type_tax_use', 'in', ['sale', 'purchase']),
        ])
        for tax in taxes:
            if (tax.vat_statement_account_id.id in statement.account_ids.ids
                    or not statement.account_ids):
                # se ho una tassa padre con figli cee_type, condidero le figlie
                if any(tax_ch for tax_ch in tax.children_tax_ids
                       if tax_ch.cee_type in ('sale', 'purchase')):

                    for tax_ch in tax.children_tax_ids:
                        if tax_ch.cee_type == 'sale':
                            self._set_debit_lines(tax_ch,
                                                  debit_line_ids,
                                                  statement)
                        elif tax_ch.cee_type == 'purchase':
                            self._set_credit_lines(tax_ch,
                                                   credit_line_ids,
                                                   statement)

                elif tax.type_tax_use == 'sale':
                    self._set_debit_lines(tax, debit_line_ids, statement)
                elif tax.type_tax_use == 'purchase':
                    self._set_credit_lines(tax, credit_line_ids, statement)

        return credit_line_ids, debit_line_ids

    @api.onchange('authority_partner_id')
    def on_change_partner_id(self):
        self.authority_vat_account_id = (
            self.authority_partner_id.property_account_payable_id.id)

    @api.onchange('interest')
    def onchange_interest(self):
        company = self.env.user.company_id
        self.interest_percent = (
            company.of_account_end_vat_statement_interest_percent)

    @api.multi
    def get_account_interest(self):
        company = self.env.user.company_id
        if (
            company.of_account_end_vat_statement_interest or
            any([s.interest for s in self])
        ):
            if not company.of_account_end_vat_statement_interest_account_id:
                raise UserError(
                    _("The account for vat interest must be configurated"))

        return company.of_account_end_vat_statement_interest_account_id


class StatementDebitAccountLine(models.Model):
    _name = 'statement.debit.account.line'
    _description = "VAT Statement debit account line"

    account_id = fields.Many2one(
        'account.account', 'Account', required=True
    )
    tax_id = fields.Many2one(
        'account.tax', 'Tax', required=True
    )
    statement_id = fields.Many2one(
        'account.vat.period.end.statement', 'VAT statement'
    )
    amount = fields.Float(
        'Amount', required=True, digits=dp.get_precision('Account')
    )


class StatementCreditAccountLine(models.Model):
    _name = 'statement.credit.account.line'
    _description = "VAT Statement credit account line"

    account_id = fields.Many2one(
        'account.account', 'Account', required=True
    )
    tax_id = fields.Many2one(
        'account.tax', 'Tax', required=True
    )
    statement_id = fields.Many2one(
        'account.vat.period.end.statement', 'VAT statement'
    )
    amount = fields.Float(
        'Amount', required=True, digits=dp.get_precision('Account')
    )


class StatementGenericAccountLine(models.Model):
    _name = 'statement.generic.account.line'
    _description = "VAT Statement generic account line"

    account_id = fields.Many2one(
        'account.account', 'Account', required=True
    )
    statement_id = fields.Many2one(
        'account.vat.period.end.statement', 'VAT statement'
    )
    amount = fields.Float(
        'Amount', required=True, digits=dp.get_precision('Account')
    )
    name = fields.Char('Description')


class AccountTax(models.Model):
    _inherit = "account.tax"
    vat_statement_account_id = fields.Many2one(
        'account.account',
        "Account used for VAT statement",
        help="The tax balance will be "
             "associated to this account after selecting the period in "
             "VAT statement"
    )


class DateRange(models.Model):
    _inherit = "date.range"
    vat_statement_id = fields.Many2one(
        'account.vat.period.end.statement', "VAT statement"
    )
