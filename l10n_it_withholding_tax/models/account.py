# Copyright 2015 Alessandro Camilli (<http://www.openforce.it>)
# Copyright 2018 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError


class AccountPartialReconcile(models.Model):
    _inherit = "account.partial.reconcile"

    @api.model
    def create(self, vals):
        # In case of WT The amount of reconcile mustn't exceed the tot net
        # amount. The amount residual will be full reconciled with amount net
        # and amount wt created with payment
        invoice = False
        ml_ids = []
        if vals.get('debit_move_id'):
            ml_ids.append(vals.get('debit_move_id'))
        if vals.get('debit_move_id'):
            ml_ids.append(vals.get('credit_move_id'))
        for ml in self.env['account.move.line'].browse(ml_ids):
            domain = [('move_id', '=', ml.move_id.id)]
            invoice = self.env['account.invoice'].search(domain)
            if invoice:
                break
        # Limit value of reconciliation
        if invoice and invoice.withholding_tax and invoice.amount_net_pay:
            # We must consider amount in foreign currency, if present
            # Note that this is always executed, for every reconciliation.
            # Thus, we must not change amount when not in withholding tax case
            amount = vals.get('amount_currency') or vals.get('amount')
            if amount > invoice.amount_net_pay:
                vals.update({'amount': invoice.amount_net_pay})

        # Create reconciliation
        reconcile = super(AccountPartialReconcile, self).create(vals)
        # Avoid re-generate wt moves if the move line is an wt move.
        # It's possible if the user unreconciles a wt move under invoice
        ld = self.env['account.move.line'].browse(vals.get('debit_move_id'))
        lc = self.env['account.move.line'].browse(vals.get('credit_move_id'))

        if lc.withholding_tax_generated_by_move_id \
                or ld.withholding_tax_generated_by_move_id:
            is_wt_move = True
        else:
            is_wt_move = False
        # Wt moves creation
        if invoice.withholding_tax_line_ids \
                and not self._context.get('no_generate_wt_move')\
                and not is_wt_move:
                # and not wt_existing_moves\
            reconcile.generate_wt_moves()

        return reconcile

    def _prepare_wt_move(self, vals):
        """
        Hook to change values before wt move creation
        """
        return vals

    @api.model
    def generate_wt_moves(self):
        wt_statement_obj = self.env['withholding.tax.statement']
        # Reconcile lines
        line_payment_ids = []
        line_payment_ids.append(self.debit_move_id.id)
        line_payment_ids.append(self.credit_move_id.id)
        domain = [('id', 'in', line_payment_ids)]
        rec_lines = self.env['account.move.line'].search(domain)

        # Search statements of competence
        wt_statements = False
        rec_line_statement = False
        for rec_line in rec_lines:
            domain = [('move_id', '=', rec_line.move_id.id)]
            wt_statements = wt_statement_obj.search(domain)
            if wt_statements:
                rec_line_statement = rec_line
                break
        # Search payment move
        rec_line_payment = False
        for rec_line in rec_lines:
            if rec_line.id != rec_line_statement.id:
                rec_line_payment = rec_line
        # Generate wt moves
        wt_moves = []
        for wt_st in wt_statements:
            amount_wt = wt_st.get_wt_competence(self.amount)
            # Date maturity
            p_date_maturity = False
            payment_lines = wt_st.withholding_tax_id.payment_term.compute(
                amount_wt,
                rec_line_payment.date or False)
            if payment_lines and payment_lines[0]:
                p_date_maturity = payment_lines[0][0][0]
            wt_move_vals = {
                'statement_id': wt_st.id,
                'date': rec_line_payment.date,
                'partner_id': rec_line_statement.partner_id.id,
                'reconcile_partial_id': self.id,
                'payment_line_id': rec_line_payment.id,
                'credit_debit_line_id': rec_line_statement.id,
                'withholding_tax_id': wt_st.withholding_tax_id.id,
                'account_move_id': rec_line_payment.move_id.id or False,
                'date_maturity':
                    p_date_maturity or rec_line_payment.date_maturity,
                'amount': amount_wt
            }
            wt_move_vals = self._prepare_wt_move(wt_move_vals)
            wt_move = self.env['withholding.tax.move'].create(wt_move_vals)
            wt_moves.append(wt_move)
            # Generate account move
            wt_move.generate_account_move()
        return wt_moves

    @api.multi
    def unlink(self):
        statements = []
        for rec in self:
            # To avoid delete if the wt move are paid
            domain = [('reconcile_partial_id', '=', rec.id),
                      ('state', '!=', 'due')]
            wt_moves = self.env['withholding.tax.move'].search(domain)
            if wt_moves:
                raise ValidationError(
                    _('Warning! Only Withholding Tax moves in Due status \
                    can be deleted'))
            # Statement to recompute
            domain = [('reconcile_partial_id', '=', rec.id)]
            wt_moves = self.env['withholding.tax.move'].search(domain)
            for wt_move in wt_moves:
                if wt_move.statement_id not in statements:
                    statements.append(wt_move.statement_id)

        res = super(AccountPartialReconcile, self).unlink()
        # Recompute statement values
        for st in statements:
            st._compute_total()
        return res


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
            wt_ids = self.pool['withholding.tax'].search(
                self.env.cr, self.env.uid, domain)
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
                            self.env.cr, self.env.uid, wt_ids[0], wt_amount)
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


class account_payment(models.Model):
    _inherit = "account.payment"

    @api.model
    def default_get(self, fields):
        """
        Redifine  amount to pay proportionally to amount total less wt
        """
        rec = super(account_payment, self).default_get(fields)
        invoice_defaults = self.resolve_2many_commands('invoice_ids',
                                                       rec.get('invoice_ids'))
        if invoice_defaults and len(invoice_defaults) == 1:
            invoice = invoice_defaults[0]
            if 'withholding_tax_amount' in invoice \
                    and invoice['withholding_tax_amount']:
                coeff_net = invoice['residual'] / invoice['amount_total']
                rec['amount'] = invoice['amount_net_pay'] * coeff_net
        return rec


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    withholding_tax_id = fields.Many2one(
        'withholding.tax', string='Withholding Tax')
    withholding_tax_base = fields.Float(string='Withholding Tax Base')
    withholding_tax_amount = fields.Float(string='Withholding Tax Amount')
    withholding_tax_generated_by_move_id = fields.Many2one(
        'account.move', string='Withholding Tax generated from', readonly=True)

    @api.multi
    def remove_move_reconcile(self):
        # When unreconcile a payment with a wt move linked, it will be
        # unreconciled also the wt account move
        for account_move_line in self:
            rec_move_ids = self.env['account.partial.reconcile']
            domain = [('withholding_tax_generated_by_move_id', '=',
                       account_move_line.move_id.id)]
            wt_mls = self.env['account.move.line'].search(domain)
            # Avoid wt move not in due state
            domain = [('wt_account_move_id', 'in',
                       wt_mls.mapped('move_id').ids)]
            wt_moves = self.env['withholding.tax.move'].search(domain)
            wt_moves.check_unlink()

            for wt_ml in wt_mls:
                rec_move_ids += wt_ml.matched_debit_ids
                rec_move_ids += wt_ml.matched_credit_ids
            rec_move_ids.unlink()
            # Delete wt move
            for wt_move in wt_mls.mapped('move_id'):
                wt_move.button_cancel()
                wt_move.unlink()

        return super(AccountMoveLine, self).remove_move_reconcile()

    @api.multi
    def prepare_move_lines_for_reconciliation_widget(
            self, target_currency=False, target_date=False):
        """
        Net amount for invoices with withholding tax
        """
        res = super(
            AccountMoveLine, self
        ).prepare_move_lines_for_reconciliation_widget(
            target_currency, target_date)
        for dline in res:
            if 'id' in dline and dline['id']:
                line = self.browse(dline['id'])
                if line.withholding_tax_amount:
                    dline['debit'] = (
                        line.debit - line.withholding_tax_amount if line.debit
                        else 0
                    )
                    dline['credit'] = (
                        line.credit - line.withholding_tax_amount
                        if line.credit else 0
                    )
                    dline['name'] += (
                        _(' (Net to pay: %s)')
                        % (dline['debit'] or dline['credit'])
                    )
        return res


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    withholding_tax_ids = fields.Many2many(
        'withholding.tax', 'account_fiscal_position_withholding_tax_rel',
        'fiscal_position_id', 'withholding_tax_id', string='Withholding Tax')


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    @api.depends(
        'invoice_line_ids.price_subtotal', 'withholding_tax_line_ids.tax',
        'currency_id', 'company_id', 'date_invoice')
    def _amount_withholding_tax(self):
        res = {}
        dp_obj = self.env['decimal.precision']
        for invoice in self:
            withholding_tax_amount = 0.0
            for wt_line in invoice.withholding_tax_line_ids:
                withholding_tax_amount += round(
                    wt_line.tax, dp_obj.precision_get('Account'))
            invoice.amount_net_pay = invoice.amount_total - \
                withholding_tax_amount
            invoice.withholding_tax_amount = withholding_tax_amount
        return res

    withholding_tax = fields.Boolean('Withholding Tax')
    withholding_tax_line_ids = fields.One2many(
        'account.invoice.withholding.tax', 'invoice_id', 'Withholding Tax',
        readonly=True, states={'draft': [('readonly', False)]})
    withholding_tax_amount = fields.Float(
        compute='_amount_withholding_tax',
        digits=dp.get_precision('Account'), string='Withholding tax',
        store=True, readonly=True)
    amount_net_pay = fields.Float(
        compute='_amount_withholding_tax',
        digits=dp.get_precision('Account'), string='Net To Pay',
        store=True, readonly=True)

    @api.model
    def create(self, vals):
        invoice = super(AccountInvoice,
                        self.with_context(mail_create_nolog=True)).create(vals)

        if any(line.invoice_line_tax_wt_ids for line in
               invoice.invoice_line_ids) \
                and not invoice.withholding_tax_line_ids:
            invoice.compute_taxes()

        return invoice

    @api.onchange('invoice_line_ids')
    def _onchange_invoice_line_wt_ids(self):
        self.ensure_one()
        wt_taxes_grouped = self.get_wt_taxes_values()
        wt_tax_lines = []
        for tax in wt_taxes_grouped.values():
            wt_tax_lines.append((0, 0, tax))
        self.withholding_tax_line_ids = wt_tax_lines
        if wt_tax_lines:
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
            for move_line in inv.move_id.line_ids:
                if move_line.account_id.internal_type not in ['receivable',
                                                              'payable']:
                    continue
                rate_num += 1
            if rate_num:
                wt_rate = round(inv.withholding_tax_amount / rate_num,
                                dp_obj.precision_get('Account'))
            wt_residual = inv.withholding_tax_amount
            # Re-read move lines to assign the amounts of wt
            i = 0
            for move_line in inv.move_id.line_ids:
                if move_line.account_id.internal_type not in ['receivable',
                                                              'payable']:
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
            for line in invoice.invoice_line_ids:
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
        for inv_wt in self.withholding_tax_line_ids:
            val = {
                'date': self.move_id.date,
                'move_id': self.move_id.id,
                'invoice_id': self.id,
                'partner_id': self.partner_id.id,
                'withholding_tax_id': inv_wt.withholding_tax_id.id,
                'base': inv_wt.base,
                'tax': inv_wt.tax,
            }
            wt_statement_obj.create(val)


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
