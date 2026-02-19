# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# Copyright 2026 Nextev Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountMoveLineInherit(models.Model):
    _inherit = "account.move.line"

    l10n_it_edi_admin_ref = fields.Char(string="Admin. ref.", size=20, copy=False)
    l10n_it_edi_other_data_ids = fields.One2many(
        "l10n_it_edi.line_other_data",
        "move_line_id",
        string="Other Management Data",
        copy=True,
        help="Additional management data (AltriDatiGestionali) to be exported "
        "in the FatturaPA XML.",
    )

    def action_open_other_data(self):
        """Open a popup to manage Other Management Data for this invoice line."""
        self.ensure_one()
        return {
            "name": "Altri Dati Gestionali",
            "type": "ir.actions.act_window",
            "res_model": "l10n_it_edi.line_other_data",
            "view_mode": "list,form",
            "domain": [("move_line_id", "=", self.id)],
            "context": {
                "default_move_line_id": self.id,
            },
            "target": "new",
        }
