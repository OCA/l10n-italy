#  Copyright 2024 Roberto Fichera - Level Prime Srl
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class FatturapaRelatedDocumentType(models.Model):
    _inherit = "fatturapa.related_document_type"

    contract_id = fields.Many2one(
        comodel_name="contract.contract",
        string="Contract",
        index=True,
        readonly=True,
    )

    contract_line_id = fields.Many2one(
        comodel_name="contract.line",
        string="Contract Line",
        index=True,
        readonly=True,
    )
