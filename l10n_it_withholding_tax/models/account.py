# -*- coding: utf-8 -*-
# Copyright © 2015 Alessandro Camilli (<http://www.openforce.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.one
    def _prepare_wt_values(self):

        partner = False
        wt_competence = {}
        # First : Partner and WT competence
        for line in self.line_id:
            if line.partner_id:
                partner = line.partner_id
                if partner.property_account_position:
                    for wt in (
                        partner.property_account_position.withholding_tax_ids
                    ):
                        wt_competence[wt.id] = {
                            'withholding_tax_id': wt.id,
                            'partner_id': partner.id,
                            'date': self.date,
                            'account_move_id': self.id,
                            'wt_account_move_line_id': False,
                            'base': 0,
                            'amount': 0,
                        }
                break
        # After : Loking for WT lines
        wt_amount = 0
        for line in self.line_id:
            domain = []
            # WT line
            if line.credit:
                domain.append(
                    ('account_payable_id', '=', line.account_id.id)
                    )
                amount = line.credit
            else:
                domain.append(
                    ('account_receivable_id', '=', line.account_id.id)
                    )
                amount = line.debit
            wt_ids = self.pool['withholding.tax'].search(self.env.cr,
                                                         self.env.uid,
                                                         domain)
            if wt_ids:
                wt_amount += amount
                if (
                    wt_competence and wt_competence[wt_ids[0]] and
                    'amount' in wt_competence[wt_ids[0]]
                ):
                    wt_competence[wt_ids[0]]['wt_account_move_line_id'] = (
                        line.id)
                    wt_competence[wt_ids[0]]['amount'] = wt_amount
                    wt_competence[wt_ids[0]]['base'] = (
                        self.pool['withholding.tax'].get_base_from_tax(
                            self.env.cr, self.env.uid,
                            wt_ids[0], wt_amount)
                    )

        wt_codes = []
        if wt_competence:
            for key, val in wt_competence.items():
                wt_codes.append(val)
        res = {
            'partner_id': partner and partner.id or False,
            'move_id': self.id,
            'invoice_id': False,
            'date': self.date,
            'base': wt_codes and wt_codes[0]['base'] or 0,
            'tax': wt_codes and wt_codes[0]['amount'] or 0,
            'withholding_tax_id': (
                wt_codes and wt_codes[0]['withholding_tax_id'] or False),
            'wt_account_move_line_id': (
                wt_codes and wt_codes[0]['wt_account_move_line_id'] or False),
            'amount': wt_codes[0]['amount'],
        }
        return res


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    withholding_tax_id = fields.Many2one(
        'withholding.tax', string='Withholding Tax')
    withholding_tax_base = fields.Float(string='Withholding Tax Base')
    withholding_tax_amount = fields.Float(string='Withholding Tax Amount')
    withholding_tax_generated_by_move_id = fields.Many2one(
        'account.move', string='Withholding Tax generated from', readonly=True)


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    withholding_tax_ids = fields.Many2many(
        'withholding.tax', 'account_fiscal_position_withholding_tax_rel',
        'fiscal_position_id', 'withholding_tax_id', string='Withholding Tax')


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    @api.depends(
        'invoice_line.price_subtotal', 'withholding_tax_line',
        'currency_id', 'company_id', 'date_invoice', 'payment_ids')
    def _amount_withholding_tax(self):
        dp_obj = self.env['decimal.precision']
        for invoice in self:
            withholding_tax_amount = 0.0
            for wt_line in invoice.withholding_tax_line:
                withholding_tax_amount += round(
                    wt_line.tax, dp_obj.precision_get('Account'))
            invoice.amount_net_pay = invoice.amount_total - \
                withholding_tax_amount
            amount_net_pay_residual = invoice.amount_net_pay
            invoice.withholding_tax_amount = withholding_tax_amount
            for line in invoice.payment_ids:
                if not line.withholding_tax_generated_by_move_id:
                    amount_net_pay_residual -= (line.debit or line.credit)
            invoice.amount_net_pay_residual = amount_net_pay_residual

    withholding_tax = fields.Boolean('Withholding Tax')
    withholding_tax_line = fields.One2many(
        'account.invoice.withholding.tax', 'invoice_id',
        'Withholding Tax Lines', copy=True,
        readonly=True, states={'draft': [('readonly', False)]})
    withholding_tax_amount = fields.Float(
        compute='_amount_withholding_tax',
        digits=dp.get_precision('Account'), string='Withholding tax Amount',
        store=True, readonly=True)
    amount_net_pay = fields.Float(
        compute='_amount_withholding_tax',
        digits_compute=dp.get_precision('Account'), string='Net To Pay',
        store=True, readonly=True)
    amount_net_pay_residual = fields.Float(
        compute='_amount_withholding_tax',
        digits=dp.get_precision('Account'), string='Residual Net To Pay',
        store=True, readonly=True)

    @api.model
    def create(self, vals):
        invoice = super(AccountInvoice,
                        self.with_context(mail_create_nolog=True)).create(vals)

        if any(line.invoice_line_tax_wt_ids for line in
               invoice.invoice_line) \
                and not invoice.withholding_tax_line:
            invoice.button_reset_taxes()

        return invoice

    @api.onchange('invoice_line')
    def _onchange_invoice_line_wt_ids(self):
        self.ensure_one()
        wt_taxes_grouped = self.get_wt_taxes_values()
        wt_tax_lines = [(5, 0, 0)]
        for tax in wt_taxes_grouped.values():
            wt_tax_lines.append((0, 0, tax))
        self.withholding_tax_line = wt_tax_lines
        if len(wt_tax_lines) > 1:
            self.withholding_tax = True
        else:
            self.withholding_tax = False

    @api.multi
    def action_move_create(self):
        '''
        Split amount withholding tax on account move lines
        '''
        dp_obj = self.env['decimal.precision']
        res = super(AccountInvoice, self).action_move_create()

        for inv in self:
            # Rates
            rate_num = 0
            for move_line in inv.move_id.line_id:
                if move_line.account_id.type not in ['receivable', 'payable']:
                    continue
                rate_num += 1
            if rate_num:
                wt_rate = round(inv.withholding_tax_amount / rate_num,
                                dp_obj.precision_get('Account'))
            wt_residual = inv.withholding_tax_amount
            # Re-read move lines to assign the amounts of wt
            i = 0
            for move_line in inv.move_id.line_id:
                if move_line.account_id.type not in ['receivable', 'payable']:
                    continue
                i += 1
                if i == rate_num:
                    wt_amount = wt_residual
                else:
                    wt_amount = wt_rate
                wt_residual -= wt_amount
                # update line
                move_line.write({'withholding_tax_amount': wt_amount})
            # Create WT Statement
            self.create_wt_statement()

        return res

    @api.multi
    def get_wt_taxes_values(self):
        tax_grouped = {}
        for invoice in self:
            for line in invoice.invoice_line:
                taxes = []
                for wt_tax in line.invoice_line_tax_wt_ids:
                    res = wt_tax.compute_tax(line.price_subtotal)
                    tax = {
                        'id': wt_tax.id,
                        'sequence': wt_tax.sequence,
                        'base': res['base'],
                        'tax': res['tax'],
                    }
                    taxes.append(tax)

                for tax in taxes:
                    val = {
                        'invoice_id': invoice.id,
                        'withholding_tax_id': tax['id'],
                        'tax': tax['tax'],
                        'base': tax['base'],
                        'sequence': tax['sequence'],
                        }

                    key = self.env['withholding.tax'].browse(
                        tax['id']).get_grouping_key(val)

                    if key not in tax_grouped:
                        tax_grouped[key] = val
                    else:
                        tax_grouped[key]['tax'] += val['tax']
                        tax_grouped[key]['base'] += val['base']
        return tax_grouped

    @api.one
    def create_wt_statement(self):
        """
        Create one statement for each withholding tax
        """
        wt_statement_obj = self.env['withholding.tax.statement']
        for inv_wt in self.withholding_tax_line:
            wt_base_amount = inv_wt.base
            wt_tax_amount = inv_wt.tax
            if self.type in ['in_refund', 'out_refund']:
                wt_base_amount = -1 * wt_base_amount
                wt_tax_amount = -1 * wt_tax_amount
            val = {
                'wt_type': '',
                'date': self.move_id.date,
                'move_id': self.move_id.id,
                'invoice_id': self.id,
                'partner_id': self.partner_id.id,
                'withholding_tax_id': inv_wt.withholding_tax_id.id,
                'base': wt_base_amount,
                'tax': wt_tax_amount,
            }
            wt_statement_obj.create(val)

    @api.v7
    def invoice_pay_customer(self, cr, uid, ids, context=None):
        res = super(AccountInvoice, self).invoice_pay_customer(
            cr, uid, ids, context)

        inv = self.browse(cr, uid, ids[0], context=context)
        if inv.withholding_tax_amount:
            res['context'].update({'default_amount': inv.amount_net_pay})
        return res

    @api.multi
    def invoice_pay_customer(self):
        self.ensure_one()
        res = super(AccountInvoice, self).invoice_pay_customer()

        if self.withholding_tax_amount:
            res['context'].update({'default_amount': self.amount_net_pay})
        return res

    @api.multi
    def compute_amount_withholding_excluded(self):
        total_withholding_tax_excluded = 0.0
        for invoice in self:
            for line in invoice.invoice_line:
                if line.withholding_tax_exclude:
                    total_withholding_tax_excluded += line.price_subtotal
            return total_withholding_tax_excluded

    @api.onchange('fiscal_position')
    def onchange_fiscal_position(self):
        use_wt = False
        if self.fiscal_position and self.fiscal_position.withholding_tax_ids:
            use_wt = True
        self.withholding_tax = use_wt

    @api.one
    def button_reset_taxes(self):
        res = super(AccountInvoice, self).button_reset_taxes()
        self._onchange_invoice_line_wt_ids()
        return res


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.model
    def _default_withholding_tax(self):
        result = []
        fiscal_position_id = self._context.get('fiscal_position_id', False)
        if fiscal_position_id:
            fp = self.env['account.fiscal.position'].browse(fiscal_position_id)
            wt_ids = fp.withholding_tax_ids.mapped('id')
            result.append((6, 0, wt_ids))
        return result

    invoice_line_tax_wt_ids = fields.Many2many(
        comodel_name='withholding.tax', relation='account_invoice_line_tax_wt',
        column1='invoice_line_id', column2='withholding_tax_id', string='W.T.',
        default=_default_withholding_tax,
    )
    withholding_tax_exclude = fields.Boolean()

    @api.multi
    def product_id_change(self, product, uom_id, qty=0, name='',
                          type='out_invoice',
                          partner_id=False, fposition_id=False,
                          price_unit=False, currency_id=False,
                          company_id=None):
        res = super(AccountInvoiceLine, self).product_id_change(
            product, uom_id, qty, name, type,
            partner_id, fposition_id, price_unit, currency_id,
            company_id)
        product_obj = self.env['product.product'].browse(product)
        res['value'].update({
            'withholding_tax_exclude': product_obj.withholding_tax_exclude})
        return res


class AccountInvoiceWithholdingTax(models.Model):
    '''
    Withholding tax lines in the invoice
    '''

    _name = 'account.invoice.withholding.tax'
    _description = 'Invoice Withholding Tax Line'

    def _prepare_price_unit(self, line):
        price_unit = 0
        price_unit = line.price_unit * \
            (1 - (line.discount or 0.0) / 100.0)
        return price_unit

    @api.depends('base', 'tax', 'invoice_id.amount_untaxed')
    def _compute_coeff(self):
        for inv_wt in self:
            if inv_wt.invoice_id.amount_untaxed:
                inv_wt.base_coeff = \
                    inv_wt.base / inv_wt.invoice_id.amount_untaxed
            if inv_wt.base:
                inv_wt.tax_coeff = inv_wt.tax / inv_wt.base

    invoice_id = fields.Many2one('account.invoice', string='Invoice',
                                 ondelete="cascade")
    withholding_tax_id = fields.Many2one('withholding.tax',
                                         string='Withholding tax',
                                         ondelete='restrict')
    sequence = fields.Integer('Sequence')
    base = fields.Float('Base')
    tax = fields.Float('Tax')
    base_coeff = fields.Float(
        'Base Coeff', compute='_compute_coeff', store=True, help="Coeff used\
         to compute amount competence in the riconciliation")
    tax_coeff = fields.Float(
        'Tax Coeff', compute='_compute_coeff', store=True, help="Coeff used\
         to compute amount competence in the riconciliation")

    @api.onchange('withholding_tax_id')
    def onchange_withholding_tax_id(self):
        if self.withholding_tax_id:
            tot_invoice = 0.0
            for inv_line in self.invoice_id.invoice_line:
                tot_invoice += inv_line.price_subtotal
            tax = self.withholding_tax_id.compute_amount(
                (tot_invoice), invoice_id=None)
            self.base = tax['base']
            self.tax = tax['tax']
