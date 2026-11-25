# Copyright 2024 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountPaymentLineInherit(models.Model):
    _inherit = "account.payment.line"

    def draft2open_payment_line_check(self):
        res = super().draft2open_payment_line_check()
        sepa_dd_lines = self.filtered(
            lambda line: line.order_id.payment_method_id.code.startswith(
                "cbi_sdd_italy"
            )
        )
        sepa_dd_lines._check_sepa_direct_debit_ready()
        return res

    def _prepare_account_payment_vals(self):
        vals = super()._prepare_account_payment_vals()
        payment_mode = self.order_id.payment_mode_id

        if payment_mode.payment_method_id.code.startswith("cbi_sdd_italy"):
            today = fields.Date.context_today(self)

            if self.order_id.date_prefered == "due":
                requested_date = self[:1].ml_maturity_date or self[:1].date or today
            elif self.order_id.date_prefered == "fixed":
                requested_date = self.order_id.date_scheduled or today
            else:
                requested_date = today
            vals["date"] = requested_date
        return vals
