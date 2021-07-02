from odoo import api, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    @api.onchange("meal_voucher_type")
    def onchange_meal_voucher_type(self):
        if self.meal_voucher_type == "paper":
            self.fiscalprinter_payment_type = "4"
