# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountMoveLineInherit(models.Model):
    _inherit = "account.move.line"

    def unlink(self):
        related_documents = self.mapped("related_document_ids")
        res = super().unlink()
        related_documents.check_unlink().unlink()
        return res
