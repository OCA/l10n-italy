#  Copyright 2020 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def unlink(self):
        related_documents = self.mapped("related_documents")
        res = super().unlink()
        related_documents.check_unlink().unlink()
        return res
