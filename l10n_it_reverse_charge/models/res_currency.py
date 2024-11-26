from odoo import models


class ResCurrency(models.BaseModel):
    _inherit = "res.currency"

    def _convert(self, from_amount, to_currency, company, date, round=True):
        if self.env.context.get("force_conversion_date"):
            return super(ResCurrency, self)._convert(
                from_amount,
                to_currency,
                company,
                date=self.env.context["force_conversion_date"],
                round=round,
            )

        return super(ResCurrency, self)._convert(
            from_amount, to_currency, company, date, round
        )
