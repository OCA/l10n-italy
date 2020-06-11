from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _enasarco_move(self):
        for line in self:
            if line.invoice_id and line.invoice_id.enasarco_move_id:
                line.enasarco_move = True
            else:
                line.enasarco_move = False

    enasarco_move = fields.Boolean('Enasarco Move', compute="_enasarco_move",
                                   store=True)

    @api.multi
    def prepare_move_lines_for_reconciliation_widget(
            self, target_currency=False, target_date=False):
        lines_data = super(
            AccountMoveLine,
            self).prepare_move_lines_for_reconciliation_widget(
            target_currency, target_date)
        for line_data in lines_data:
            if not line_data.get('id', False):
                continue
            line = self.browse(line_data['id'])
            # Recalculate values considering enasarco amount
            if line.invoice_id and line.invoice_id.enasarco_amount_total:
                line_data['debit'] = \
                    (line_data['debit'] -
                     line.invoice_id.enasarco_amount_total) \
                    if line_data['debit'] else 0.0
                line_data['credit'] = \
                    (line_data['credit'] -
                     line.invoice_id.enasarco_amount_total) \
                    if line_data['credit'] else 0.0
                # Replace net to pay value set by witholding tax module
                net_to_pay_string = _('(Net to pay: %s)') % (
                    line_data['debit'] or line_data['credit'])
                if '(Net to pay:' in line_data['name']:
                    line_data['name'] = re.sub(
                        r'\(Net to pay: .+\)',
                        '',
                        line_data['name']) + net_to_pay_string
                else:
                    line_data['name'] = line_data['name'] + net_to_pay_string
                # FYI Enasarco is used only in the some company currency
                # context. So, it's not important to recalculate amount
                # in another currency value
        return lines_data


class AccountPartialReconcile(models.Model):
    _inherit = "account.partial.reconcile"

    @api.model
    def create(self, vals):
        ml_ids = []
        # If enasarco move, it will disable wt generation
        if vals.get('debit_move_id'):
            ml_ids.append(vals.get('debit_move_id'))
        if vals.get('credit_move_id'):
            ml_ids.append(vals.get('credit_move_id'))
        domain = [('id', 'in', ml_ids), ('enasarco_move', '=', True)]
        enasarco_lines = self.env['account.move.line'].search(domain)
        if enasarco_lines:
            self = self.with_context(no_generate_wt_move=True)
        return super(AccountPartialReconcile, self).create(vals)


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
            if 'enasarco_amount' in invoice \
                    and invoice['enasarco_amount']:
                coeff_net = (invoice['residual'] + invoice['enasarco_amount'])\
                     / invoice['amount_total']
                rec['amount'] = invoice['amount_net_pay'] * coeff_net
        return rec


class account_register_payments(models.TransientModel):
    _inherit = "account.register.payments"

    @api.model
    def get_amount_residual(self, invoice):
        amount_residual = super(account_register_payments, self)\
            .get_amount_residual(invoice)
        if invoice.withholding_tax_amount or invoice.enasarco_amount:
            coeff_net = (invoice.residual + invoice.enasarco_amount) \
                / invoice.amount_total
            amount_residual = invoice.amount_net_pay * coeff_net
            return amount_residual
        return False
