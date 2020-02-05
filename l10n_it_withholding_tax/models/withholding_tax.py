# -*- coding: utf-8 -*-
# Copyright © 2015 Alessandro Camilli (<http://www.openforce.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
from openerp import netsvc


class WithholdingTax(models.Model):
    _name = 'withholding.tax'
    _description = 'Withholding Tax'

    active = fields.Boolean('Active', default=True)
    name = fields.Char('Name', size=256, required=True)
    certification = fields.Boolean('Certification')
    comment = fields.Text('Text')
    account_receivable_id = fields.Many2one(
        'account.account',
        'Account Receivable', required=True,
        domain=[('type', '=', 'receivable')])
    account_payable_id = fields.Many2one(
        'account.account',
        'Account Payable', required=True, domain=[('type', '=', 'payable')])
    payment_term = fields.Many2one('account.payment.term', 'Payment Terms',
                                   required=True)
    tax = fields.Float(string='Tax %', compute='_compute_withholding')
    base = fields.Float(string='Base', compute='_compute_withholding')
    rate_ids = fields.One2many('withholding.tax.rate', 'withholding_tax_id',
                               'Rates', required=True)

    @api.one
    @api.depends('rate_ids.date_start', 'rate_ids.date_stop',
                 'rate_ids.base', 'rate_ids.tax')
    def _compute_withholding(self):
        rate_domain = [
            ('withholding_tax_id', '=', self.id),

            '|',
            ('date_start', '<=', fields.Date.today()),
            ('date_start', '=', False),

            '|',
            ('date_stop', '>=', fields.Date.today()),
            ('date_stop', '=', False),
        ]

        rate = self.env['withholding.tax.rate'].search(rate_domain, limit=1,
                                                       order='date_start ASC')

        self.tax = rate and rate.tax or 0.0
        self.base = rate and rate.base or 1.0

    def compute_amount(self, amount_invoice, invoice_id=None):
        invoice_obj = self.env['account.invoice']
        res = {
            'base': 0,
            'tax': 0
        }
        if not amount_invoice and invoice_id:
            invoice = invoice_obj.browse(invoice_id)
            total_withholding_tax_excluded = \
                invoice.compute_amount_withholding_excluded()
            amount_invoice = (
                invoice.amount_untaxed - total_withholding_tax_excluded)
        # v7->v8 removed tax = self.browse(cr, uid, withholding_tax_id)
        base = amount_invoice * self.base
        tax = base * ((self.tax or 0.0) / 100.0)

        res['base'] = base
        res['tax'] = tax

        return res

    @api.one
    def get_base_from_tax(self, wt_amount):
        """
        100 * wt_amount        1
        ---------------  *  -------
              % tax          Coeff
        """
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
            domain = [
                ('withholding_tax_id', '=', self.withholding_tax_id.id),
                ('id', '!=', self.id)]
            if self.date_start:
                domain.extend([
                    '|',
                    ('date_stop', '>=', self.date_start),
                    ('date_stop', '=', False)])
            if self.date_stop:
                domain.extend([
                    '|',
                    ('date_start', '<=', self.date_stop),
                    ('date_start', '=', False)])

            overlapping_rate = self.env['withholding.tax.rate'].search(domain, limit=1)
            if overlapping_rate:
                raise ValidationError(
                    _('Error! You cannot have 2 rates that overlap!'))

    withholding_tax_id = fields.Many2one('withholding.tax',
                                         string='Withholding Tax',
                                         ondelete='cascade', readonly=True)
    date_start = fields.Date(string='Date Start')
    date_stop = fields.Date(string='Date Stop')
    comment = fields.Text(string='Text')
    base = fields.Float(string='Base Coeff.', default=1)
    tax = fields.Float(string='Tax %')


class WithholdingTaxStatement(models.Model):

    """
    The Withholding tax statement are created at the invoice validation
    """

    _name = 'withholding.tax.statement'
    _description = 'Withholding Tax Statement'

    @api.multi
    @api.depends('move_ids.amount', 'move_ids.state')
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
    base = fields.Float('Base')
    tax = fields.Float('Tax')
    amount = fields.Float(string='WT amount', store=True, readonly=True,
                          compute='_compute_total')
    amount_paid = fields.Float(string='WT amount paid', store=True,
                               readonly=True, compute='_compute_total')
    move_ids = fields.One2many('withholding.tax.move',
                               'statement_id', 'Moves')
    display_name = fields.Char(
        string='Name', compute='_compute_display_name',
    )

    @api.multi
    def _compute_display_name(self):
        for st in self:
            name = '%s - %s' % (st.partner_id.name,
                                st.withholding_tax_id and
                                st.withholding_tax_id.name or '')
            st.display_name = name


class WithholdingTaxMove(models.Model):

    """
    The Withholding tax moves are created at the payment of invoice using
    voucher
    """
    _name = 'withholding.tax.move'
    _description = 'Withholding Tax Move'

    state = fields.Selection([
        ('due', 'Due'),
        ('paid', 'Paid'),
    ], 'Status', readonly=True, copy=False, select=True,
        default='due')
    statement_id = fields.Many2one('withholding.tax.statement', 'Statement')
    date = fields.Date('Date Competence')
    wt_voucher_line_id = fields.Many2one('withholding.tax.voucher.line',
                                         'WT Account Voucher Line',
                                         ondelete='cascade')
    move_line_id = fields.Many2one(
        'account.move.line', 'Account Move line',
        ondelete='cascade', help="Used from trace WT from other parts(BS)")
    withholding_tax_id = fields.Many2one('withholding.tax', 'Withholding Tax')
    amount = fields.Float('Amount')
    partner_id = fields.Many2one('res.partner', 'Partner')
    date_maturity = fields.Date('Date Maturity')
    account_move_id = fields.Many2one('account.move', 'Account Move',
                                      ondelete='cascade')
    display_name = fields.Char(
        string='Name', compute='_compute_display_name',
    )

    @api.multi
    def _compute_display_name(self):
        for move in self:
            name = '%s - %s' % (move.partner_id.name,
                                move.withholding_tax_id and
                                move.withholding_tax_id.name or '')
            move.display_name = name

    @api.multi
    def action_paid(self):
        for pt in self:
            wf_service = netsvc.LocalService("workflow")
            wf_service.trg_validate(self.env.uid, self._name, pt.id, 'paid',
                                    self.env.cr)
        return True

    @api.multi
    def action_set_to_draft(self):
        for pt in self:
            wf_service = netsvc.LocalService("workflow")
            wf_service.trg_validate(self.env.uid, self._name, pt.id, 'cancel',
                                    self.env.cr)
        return True

    @api.multi
    # def move_paid(self, cr, uid, ids, *args):
    def move_paid(self):
        for move in self:
            if move.state in ['due']:
                move.write({'state': 'paid'})
        return True

    @api.multi
    # def move_set_due(self, cr, uid, ids, *args):
    def move_set_due(self):
        for move in self:
            if move.state in ['paid']:
                move.write({'state': 'due'})
        return True

    @api.multi
    def unlink(self):
        # To avoid if move is linked to voucher
        for move in self:
            if move.wt_voucher_line_id \
                    and move.wt_voucher_line_id.voucher_line_id:
                raise ValidationError(
                    _('Warning! You cannot delet move linked to voucher.You \
                    must before delete the voucher.'))
        return super(WithholdingTaxMove, self).unlink()
