#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.tools import float_compare, float_is_zero


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    @api.model
    def _get_wizard_values_from_batch(self, batch_result):
        wizard_values_from_batch = super()._get_wizard_values_from_batch(batch_result)
        self._inject_withholding_net_pay_residual(wizard_values_from_batch)
        return wizard_values_from_batch

    def _inject_withholding_net_pay_residual(self, wizard_values_from_batch):
        """If the payment is for Invoices having Withholding Taxes,
        set the Residual Net To Pay as the amount to be paid.
        """
        if self.env.context.get("active_model") == "account.move":
            moves_ids = self.env.context.get("active_ids", [])
            moves = self.env["account.move"].browse(moves_ids)
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
        residual_amount_precision = self.env["decimal.precision"].precision_get(
            "Account"
        )
        residual_withholding_amount = sum(
            self.mapped("line_ids.move_id.amount_residual") or []
        ) - sum(self.mapped("line_ids.move_id.amount_net_pay_residual") or [])
        if residual_withholding_amount:
            payment_difference = 0
            if self.source_currency_id == self.currency_id and (
                not float_compare(
                    self.source_amount_currency,
                    self.amount,
                    precision_digits=residual_amount_precision,
                )
                == 0
            ):
                payment_difference = (
                    self.source_amount_currency
                    - residual_withholding_amount
                    - self.amount
                )
            elif self.currency_id == self.company_id.currency_id and (
                not float_compare(
                    self.source_amount,
                    self.amount,
                    precision_digits=residual_amount_precision,
                )
                == 0
            ):
                # probably not needed as withholding amount does not know currency
                # Payment expressed on the company's currency.
                payment_difference = (
                    self.source_amount - residual_withholding_amount - self.amount
                )
            if (
                not self.currency_id.is_zero(payment_difference)
                and self.payment_difference_handling == "reconcile"
            ):
                payment_vals["write_off_line_vals"] = {
                    "name": self.writeoff_label,
                    "amount": payment_difference,
                    "account_id": self.writeoff_account_id.id,
                }
        return payment_vals
