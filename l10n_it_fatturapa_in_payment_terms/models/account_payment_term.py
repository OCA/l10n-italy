# Copyright 2025 Lorenzo Battistini
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    fatturapa_retrieve_due_dates = fields.Boolean(
        string="Retrieve due dates from XML",
        help="If set, payment terms will be retrieved from the XML "
             "when creating invoices from electronic invoices."
    )

    @api.one
    def compute(self, value, date_ref=False):
        """Override to use forced payment lines from XML if provided."""
        if self.env.context.get('force_totlines'):
            # Return the forced payment lines from XML
            payment_data = self.env.context.get('force_totlines')
            result = []
            for payment in payment_data:
                # Handle both dates and False (no due date)
                date_str = fields.Date.to_string(payment['date']) if payment['date'] else False
                result.append((date_str, payment['amount']))
            return result

        # Otherwise use standard computation
        # NB: api.one means that self is always a single record
        return super(AccountPaymentTerm, self).compute(value, date_ref)[0]
