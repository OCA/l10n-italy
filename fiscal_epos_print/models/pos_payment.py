from odoo import models


class PosPayment(models.Model):
    _inherit = "pos.payment"

    def _export_for_ui(self, payment):
        res = super()._export_for_ui(payment)
        res[
            "fiscalprinter_payment_type"
        ] = payment.payment_method_id.fiscalprinter_payment_type
        res[
            "fiscalprinter_payment_index"
        ] = payment.payment_method_id.fiscalprinter_payment_index
        return res
