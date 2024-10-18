# Copyright 2024 Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools import html2plaintext


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

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def _l10n_it_edi_get_values(self, pdf_values=None):
        res = super()._l10n_it_edi_get_values(pdf_values)

        causale_list = []
        if self.narration:
            try:
                narration_text = html2plaintext(self.narration)
            except Exception:
                narration_text = ""

            # max length of Causale is 200
            for causale in narration_text.split("\n"):
                if not causale:
                    continue
                causale_list_200 = [
                    causale[i : i + 200] for i in range(0, len(causale), 200)
                ]
                for causale200 in causale_list_200:
                    causale_list.append(causale200)

        res["causale"] = causale_list

        return res
