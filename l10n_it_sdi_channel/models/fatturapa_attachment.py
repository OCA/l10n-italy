#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FatturaPAAttachment(models.AbstractModel):
    _inherit = "fatturapa.attachment"

    channel_id = fields.Many2one(
        comodel_name="sdi.channel", related="company_id.sdi_channel_id", store=True
    )
