# Copyright 2024 Nextev Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


# -------------------------------------------------------
#        RIBA PAYMENT DATE
# -------------------------------------------------------
class RibaPaymentDate(models.TransientModel):
    _name = "riba.payment.date"
    _description = "RiBa Payment Date"

    date = fields.Date(string="Payment Date", required=True)

    def set_riba_payment_date(self):
        active_id = self.env.context.get("active_id", False)
        if not active_id:
            raise UserError(_("No active ID found."))
        move = self.env["account.move"].browse([active_id])
        move.date = self.date
