from odoo import api, fields, models


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    @api.depends(
        "source_amount",
        "source_amount_currency",
        "source_currency_id",
        "company_id",
        "currency_id",
        "payment_date",
        "journal_id",
    )
    def _compute_amount(self):
        for wizard in self:
            new_amount = False
            if wizard.source_currency_id == wizard.currency_id:
                # Same currency.
                if not wizard.amount or wizard.amount == wizard.source_amount_currency:
                    new_amount = wizard.source_amount_currency
            elif wizard.currency_id == wizard.company_id.currency_id:
                # Payment expressed on the company's currency.
                if not wizard.amount or wizard.amount == wizard.source_amount:
                    new_amount = wizard.source_amount
            else:
                # Foreign currency on payment different than the one set on the journal entries.
                amount_payment_currency = wizard.company_id.currency_id._convert(
                    wizard.source_amount,
                    wizard.currency_id,
                    wizard.company_id,
                    wizard.payment_date or fields.Date.today(),
                )
                new_amount = amount_payment_currency
            if new_amount:
                wizard.amount = new_amount
