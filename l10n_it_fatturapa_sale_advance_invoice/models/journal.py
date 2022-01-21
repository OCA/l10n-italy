# Copyright 2022 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class AccountJournal(models.Model):
    _inherit = "account.journal"

    advance_fiscal_document_type_id = fields.Many2one(
        comodel_name='fiscal.document.type',
    )
