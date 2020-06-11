from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    def _amount_withholding_tax(self):
        res = super(AccountInvoice, self)._amount_withholding_tax()
        for invoice in self:
            invoice.amount_net_pay = invoice.amount_net_pay - \
                invoice.enasarco_amount
        return res

    enasarco = fields.Boolean(string='Enasarco', readonly=True,
        states={'draft': [('readonly', False)]})
    enasarco_amount = fields.Monetary(string='Enasarco amount', 
        readonly=True, states={'draft': [('readonly', False)]},
        track_visibility='onchange')
    enasarco_date = fields.Date(string='Enasarco date', 
        readonly=True, states={'draft': [('readonly', False)]},
        help="Date for account move")
    enasarco_move_id = fields.Many2one(
        'account.move', string='Enasarco Account Move', 
        readonly=True, states={'draft': [('readonly', False)]},
        copy=False)
    enasarco_amount_total = fields.Monetary(string='Enasarco amount', 
        related='enasarco_amount')

    @api.multi
    def action_invoice_cancel(self):
        """
        Delete Enasarco Move
        """
        for invoice in self:
            if invoice.enasarco_move_id:
                invoice.enasarco_move_id.line_ids.remove_move_reconcile()
                invoice.enasarco_move_id.button_cancel()
                invoice.enasarco_move_id.unlink()
        super(AccountInvoice, self).action_invoice_cancel()

    @api.onchange('date')
    def enasarco_onchange_date(self):
        for inv in self:
            if inv.date:
                inv.enasarco_date = inv.date

    @api.multi
    def action_invoice_open(self):
        super(AccountInvoice, self).action_invoice_open()
        for invoice in self:
            # Verify configuration
            if not invoice.company_id.enasarco_account_id:
                raise ValidationError(
                    _('Missing Enasarco Account in the company configuration'))
            if not invoice.company_id.enasarco_journal_id:
                raise ValidationError(
                    _('Missing Enasarco journal in the company configuration'))
            enasarco_journal_id = invoice.company_id.enasarco_journal_id \
                or False
            enasarco_account_id = invoice.company_id.enasarco_account_id \
                or False

            # Lines to reconcile:
            domain = [('move_id', '=', invoice.move_id.id),
                      ('account_id.user_type_id.type', '=', 'payable'),
                      ('reconciled', '=', False)]
            lines_inv_to_reconcile = self.env[
                'account.move.line'].search(domain)

            # Enasarco registration
            if invoice.enasarco and invoice.enasarco_amount:
                lines_vals = []
                # Line for reconciliation
                values_line = {
                    'name': _('Enasarco per {}'
                              .format(invoice.number)),
                    'partner_id': invoice.partner_id.id,
                    'account_id': invoice.account_id.id,
                    'debit': invoice.enasarco_amount,
                    'credit': 0,
                    'enasarco_move': True,
                }
                lines_vals.append((0, 0, values_line))
                # Line for Enasarco debit
                values_line = {
                    'name': _('Enasarco per {} - {}'
                             .format(invoice.number,
                                     invoice.partner_id.name)),
                    'partner_id': False,
                    'account_id': enasarco_account_id.id,
                    'debit': 0,
                    'credit': invoice.enasarco_amount,
                    'enasarco_move': True,
                }
                lines_vals.append((0, 0, values_line))

                values_move = {
                    'date': invoice.enasarco_date or invoice.date,
                    'journal_id': enasarco_journal_id.id,
                    'ref': _('Enasarco per {} - {}'
                             .format(invoice.number,
                                     invoice.partner_id.name)),
                    'line_ids': lines_vals,
                }
                account_move = self.env['account.move'].create(values_move)
                invoice.enasarco_move_id = account_move.id 
                account_move.post()
                # line to rec
                domain = [('move_id', '=', account_move.id),
                      ('debit', '>', 0)]
                ml_to_rec = self.env['account.move.line'].search(domain)

                # Riconcilio il giroconto con la fattura per far simulare il
                # pagamento facendo fare la registrazione di iva per cassa
                # a Odoo
                lines_to_reconcile = lines_inv_to_reconcile + ml_to_rec
                res = lines_to_reconcile.with_context(
                    no_generate_wt_move = True).reconcile()

