#  Copyright 2020 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountInvoiceLine (models.Model):
    _inherit = 'account.invoice.line'

    @api.multi
    def unlink(self):
        # Use sudo because current user might not be able to
        # read the related documents
        # but they should be unlinked just the same
        self_sudo = self.sudo()
        related_documents = self_sudo.mapped('related_documents')
        res = super().unlink()
        related_documents.check_unlink().unlink()
        return res
