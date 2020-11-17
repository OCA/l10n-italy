# -*- coding: utf-8 -*-
# Copyright © 2015 Alessandro Camilli (<http://www.openforce.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
from openerp import netsvc


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
                 and (date_stop >= current_date or date_stop is null)
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
            [("code", "=", _('MISC'))])
        if misc_journal:
            return misc_journal[0]
        return False

    active = fields.Boolean('Active', default=True)
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company', required=True,
        default=lambda self: self.env['res.company'].browse(
            self.env['res.company']._company_default_get('l10n_it_withholding_tax')
        )
    )
    name = fields.Char('Name', size=256, required=True)
    code = fields.Char('Code', size=256, required=True)
    certification = fields.Boolean('Certification')
    comment = fields.Text('Text')
    sequence = fields.Integer('Sequence')
    account_receivable_id = fields.Many2one(
        'account.account',
        string='Account Receivable', required=True)
    account_payable_id = fields.Many2one(
        'account.account',
        string='Account Payable', required=True)
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

    wt_types = fields.Selection([
        ('enasarco', 'Enasarco tax'),
        ('ritenuta', 'Withholding tax'),
        ('inps', 'Inps Tax'),
        ('enpam', 'Enpam Tax'),
        ('other', 'Other Tax')
    ], 'Withholding tax type', required=True, default='ritenuta')
    use_daticassaprev = fields.Boolean(
        "DatiCassa export",
        help="Setting this, while exporting e-invoice XML, "
             "data will be also added to DatiCassaPrevidenziale"
    )
    daticassprev_tax_id = fields.Many2one('account.tax')

    @api.one
    @api.constrains('rate_ids')
    def _check_rate_ids(self):
        if not self.rate_ids:
            raise ValidationError(
                _('Error! Rates are required'))

    @api.multi
    def name_get(self):
        return [(w.id, w.code if w.code else '' + ' - ' + w.name) for w in self]

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        results = super(WithholdingTax, self).name_search(
            name, args=args, operator=operator, limit=limit)

        if name and not results:
            domain = args + [('code', operator, name)]
            res = self.search(domain, limit=limit)
            results = res.name_get()

        return results

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
        base = currency.round(amount * self.base)
        tax = currency.round(base * ((self.tax or 0.0) / 100.0))
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

            overlapping_rate = self.env['withholding.tax.rate'] \
                .search(domain, limit=1)
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

    '''
    The Withholding tax statement are created at the invoice validation
    '''

    _name = 'withholding.tax.statement'
    _description = 'Withholding Tax Statement'
    _order = 'id desc'

    @api.multi
    @api.depends('move_ids.amount', 'move_ids.state',)
    #  'move_ids.reconcile_partial_id')
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
    wt_type = fields.Selection([
        ('in', 'In'),
        ('out', 'Out'),
    ], 'Type', store=True, compute='_compute_type')
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

    @api.depends('move_id.line_id.account_id.user_type.name')
    def _compute_type(self):
        for st in self:
            if st.move_id:
                domain = [
                    ('move_id', '=', st.move_id.id),
                    ('account_id.user_type.name', '=', 'payable')]
                lines = self.env['account.move.line'].search(domain)
                if lines:
                    st.wt_type = 'in'
                else:
                    st.wt_type = 'out'

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
                if st.invoice_id.type in ['in_refund', 'out_refund']:
                    amount_wt = -1 * amount_wt
            elif st.move_id:
                tax_data = st.withholding_tax_id.compute_tax(amount_reconcile)
                amount_wt = tax_data['tax']
            return amount_wt

    def _compute_display_name(self):
        self.display_name = \
            self.partner_id.name + ' - ' + self.withholding_tax_id.name


class WithholdingTaxMove(models.Model):

    '''
    The Withholding tax moves are created at the payment of invoice
    '''
    _name = 'withholding.tax.move'
    _description = 'Withholding Tax Move'
    _order = 'id desc'

    state = fields.Selection([
        ('due', 'Due'),
        ('paid', 'Paid'),
    ], 'Status', readonly=True, copy=False, default='due')
    statement_id = fields.Many2one('withholding.tax.statement', 'Statement')
    wt_type = fields.Selection([
        ('in', 'In'),
        ('out', 'Out'),
    ], 'Type', store=True, related='statement_id.wt_type')
    date = fields.Date('Date Competence')
    wt_voucher_line_id = fields.Many2one('withholding.tax.voucher.line',
                                         'WT Account Voucher Line',
                                         ondelete='cascade')
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
    display_name = fields.Char(compute='_compute_display_name')

    def _compute_display_name(self):
        self.display_name = \
            self.partner_id.name + ' - ' + self.withholding_tax_id.name

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
