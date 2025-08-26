# Copyright 2025 Lorenzo Battistini
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, _
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def _get_payment_data_from_fatturapa(self):
        """Extract payment data from fatturapa.payment.data model."""
        self.ensure_one()
        payment_data = []
        payment_data_records = self.fatturapa_payments

        for payment_data_record in payment_data_records:
            for payment_detail in payment_data_record.payment_methods:
                if payment_detail.payment_due_date and payment_detail.payment_amount:
                    payment_data.append({
                        'date': payment_detail.payment_due_date,
                        'amount': -payment_detail.payment_amount
                    })

        # Check if payment total is less than e_invoice_amount_total
        if payment_data and self.e_invoice_amount_total:
            payment_total = sum(abs(p['amount']) for p in payment_data)
            e_invoice_total = abs(self.e_invoice_amount_total)

            # Use currency precision for comparison
            precision = self.currency_id.rounding or 0.01
            if payment_total + precision < e_invoice_total:
                # Add a line without due date for the remaining amount
                remaining_amount = e_invoice_total - payment_total
                payment_data.append({
                    'date': False,  # No due date
                    'amount': -remaining_amount
                })

        return payment_data

    @api.multi
    def action_move_create(self):
        """Override to use payment terms from XML if configured."""
        # Process each invoice individually to maintain context
        for invoice in self:
            # Check if payment term is configured to retrieve due dates from XML
            if invoice.payment_term_id and invoice.payment_term_id.fatturapa_retrieve_due_dates:
                payment_data = invoice._get_payment_data_from_fatturapa()
                if payment_data:
                    # Process this invoice with its specific payment data context
                    super(AccountInvoice, invoice.with_context(force_totlines=payment_data)).action_move_create()
                else:
                    # No payment data found, use standard processing
                    super(AccountInvoice, invoice).action_move_create()
            else:
                # Standard processing for invoices without XML payment terms
                super(AccountInvoice, invoice).action_move_create()
        
        return True