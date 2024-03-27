import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class AccountPaymentLine(models.Model):
    _inherit = "account.payment.line"

    line_sequence = fields.Integer(string="#", compute="_compute_line_sequence")

    def _compute_line_sequence(self):
        for _id, record in enumerate(self.order_id.payment_line_ids):
            record.line_sequence = _id + 1
