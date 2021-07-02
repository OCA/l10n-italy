from odoo import models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _payment_fields(self, ui_paymentline):
        res = super()._payment_fields(ui_paymentline)
        res["tickets_number"] = ui_paymentline.get("tickets_number", False)
        return res

    def _prepare_bank_statement_line_payment_values(self, data):
        res = super()._prepare_bank_statement_line_payment_values(data)
        res["pos_tickets_number"] = data.get("tickets_number", False)
        return res
