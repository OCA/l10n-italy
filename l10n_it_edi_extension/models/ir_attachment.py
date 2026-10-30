# Copyright 2026 Luca Orioli <lucaorioli@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.exceptions import UserError


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    def unlink(self):
        self._l10n_it_edi_ext_check_doc_attachments_unlink()
        return super().unlink()

    def _l10n_it_edi_ext_check_doc_attachments_unlink(self):
        """Forbid deleting files still listed in e-invoice attachments.

        The list would lose them silently, and with them the <Allegati> nodes
        of the invoices: the files must be removed from the list first. This
        covers the delete button of the chatter, which shows the listed files,
        and documents shared by several invoices.
        """
        if not self:
            return
        moves = (
            self.env["account.move"]
            .sudo()
            .search([("l10n_it_edi_ext_doc_attachment_ids", "in", self.ids)])
        )
        if moves:
            listed = self & moves.l10n_it_edi_ext_doc_attachment_ids
            raise UserError(
                self.env._(
                    "%(files)s cannot be deleted: listed in the e-invoice attachments "
                    "of %(moves)s. Remove them from the list first.",
                    files=", ".join(listed.sudo().mapped("name")),
                    moves=", ".join(moves.mapped("display_name")),
                )
            )
