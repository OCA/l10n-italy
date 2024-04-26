# Copyright 2024 Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    l10n_it_edi_attachment_preview_link = fields.Char(
        string="Preview link",
        compute="_compute_l10n_it_edi_attachment_preview_link",
    )

    # -------------------------------------------------------------------------
    # Computes
    # -------------------------------------------------------------------------

    @api.depends("l10n_it_edi_attachment_id")
    def _compute_l10n_it_edi_attachment_preview_link(self):
        for move in self:
            if move.l10n_it_edi_attachment_id:
                move.l10n_it_edi_attachment_preview_link = (
                    move.get_base_url()
                    + f"/fatturapa/preview/{move.l10n_it_edi_attachment_id.id}"
                )
            else:
                move.l10n_it_edi_attachment_preview_link = ""

    # -------------------------------------------------------------------------
    # Business actions
    # -------------------------------------------------------------------------

    def action_l10n_it_edi_attachment_preview(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_url",
            "name": "Show preview",
            "url": self.l10n_it_edi_attachment_preview_link,
            "target": "new",
        }
