#  Copyright 2023 Simone Rubino - TAKOBI
#  Copyright 2025 Simone Rubino - PyTech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.tools import float_is_zero


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    @api.model
    def _get_wizard_values_from_batch(self, batch_result):
        wizard_values_from_batch = super()._get_wizard_values_from_batch(batch_result)
        self._inject_withholding_net_pay_residual(
            wizard_values_from_batch, batch_result
        )
        return wizard_values_from_batch

    def _inject_withholding_net_pay_residual(
        self, wizard_values_from_batch, batch_result
    ):
        """If the payment is for Invoices having Withholding Taxes,
        set the Residual Net To Pay as the amount to be paid.
        """
        if self.env.context.get("active_model") == "account.move":
            moves = batch_result.get("lines").mapped("move_id")
            withholding_moves = moves.filtered("withholding_tax")
            if withholding_moves:
                net_pay_residual_amount = sum(
                    withholding_moves.mapped("amount_net_pay_residual")
                )
                residual_amount_precision = self.env["decimal.precision"].precision_get(
                    "Account"
                )
                if not float_is_zero(
                    net_pay_residual_amount,
                    precision_digits=residual_amount_precision,
                ):
                    wizard_values_from_batch["source_amount"] = net_pay_residual_amount
                    wizard_values_from_batch[
                        "source_amount_currency"
                    ] = net_pay_residual_amount
        return wizard_values_from_batch

    def _create_payment_vals_from_wizard(self):
        payment_vals = super()._create_payment_vals_from_wizard()
        write_off_vals = payment_vals.get("write_off_line_vals")
        if write_off_vals:
            withholding_moves = self.line_ids.move_id.filtered("withholding_tax")
            if withholding_moves:
                residual_withholding_amount = sum(
                    withholding_moves.mapped("amount_residual") or []
                ) - sum(withholding_moves.mapped("amount_net_pay_residual") or [])
                if residual_withholding_amount:
                    write_off_vals["amount"] -= residual_withholding_amount
        return payment_vals
