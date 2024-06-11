# Copyright (C) 2024 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class RibaDueDateSettlement(models.TransientModel):
    _name = "riba.due.date.settlement"
    _description = "Riba Due Date Settlement"

    due_date = fields.Date()

    def due_date_settlement_confirm(self):
        active_ids = self.env.context.get("active_ids", False)
        if not active_ids:
            raise UserError(_("No active ID found."))
        riba_ids = self.env["riba.distinta"].browse(active_ids)
        riba_lines = riba_ids.mapped("line_ids").filtered(
            lambda rl: rl.state == "accredited" and rl.due_date == self.due_date
        )
        riba_lines.riba_line_settlement()
