# Copyright (C) 2024 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class RibaDueDateSettlement(models.TransientModel):
    _name = "riba.due.date.settlement"
    _inherit = "riba.payment.multiple"
    _description = "Riba Due Date Settlement"

    due_date = fields.Date()

    def due_date_settlement_confirm(self):
        active_ids = self.env.context.get("active_ids", False)
        if not active_ids:
            raise UserError(_("No active ID found."))
        riba_lines = self.riba_line_ids.filtered(
            lambda rl: rl.due_date == self.due_date
        )
        riba_lines.riba_line_settlement(
            date=self.payment_date,
        )
