#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import UserError


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
                currency = withholding_moves.currency_id
                if len(currency) > 1:
                    raise UserError(_("Invoices must have the same currency"))
                net_pay_residual_amount = sum(
                    withholding_moves.mapped("amount_net_pay_residual")
                )
                if not currency.is_zero(
                    net_pay_residual_amount,
                ):
                    wizard_values_from_batch["source_amount"] = net_pay_residual_amount
                    # Withholding tax amount is a simple float
                    # and does not change for different currencies
                    wizard_values_from_batch[
                        "source_amount_currency"
                    ] = net_pay_residual_amount
        return wizard_values_from_batch

    def _get_total_amount_in_wizard_currency_to_full_reconcile(
        self, batch_result, early_payment_discount=True
    ):
        amount, mode = super()._get_total_amount_in_wizard_currency_to_full_reconcile(
            batch_result, early_payment_discount=early_payment_discount
        )
        withholding_net_pay_residual_values = self._inject_withholding_net_pay_residual(
            dict()
        )
        withholding_net_pay_residual = withholding_net_pay_residual_values.get(
            "source_amount"
        )
        if withholding_net_pay_residual is not None:
            amount = withholding_net_pay_residual
        return amount, mode
