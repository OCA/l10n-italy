from odoo import models


class BankRecWidget(models.Model):
    _inherit = "bank.rec.widget"

    def _lines_widget_prepare_aml_line(self, aml, **kwargs):
        self.ensure_one()

        if (
            aml.amount_residual != aml.withholding_tax_amount_net_pay_residual
            and aml.move_id.is_invoice()
        ):
            kwargs["balance"] = -aml.withholding_tax_amount_net_pay_residual
            kwargs["amount_currency"] = -aml.withholding_tax_amount_net_pay_residual
            kwargs[
                "source_amount_currency"
            ] = -aml.withholding_tax_amount_net_pay_residual
            kwargs["source_balance"] = -aml.withholding_tax_amount_net_pay_residual

        return super()._lines_widget_prepare_aml_line(aml, **kwargs)
