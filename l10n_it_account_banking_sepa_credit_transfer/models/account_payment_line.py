import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class AccountPaymentLine(models.Model):
    _inherit = "account.payment.line"

    line_sequence = fields.Integer(string="#", compute="_compute_line_sequence")

    def _compute_line_sequence(self):
        for record in self:
            line_sequence = record.order_id.payment_line_ids.ids.index(record.id) + 1
            record.line_sequence = line_sequence
