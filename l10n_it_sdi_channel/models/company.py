# Copyright 2018 Sergio Corato (https://efatto.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    sdi_channel_id = fields.Many2one("sdi.channel", string="ES channel")
    sdi_channel_type = fields.Selection(
        related="sdi_channel_id.channel_type", readonly=True
    )


class AccountConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    sdi_channel_id = fields.Many2one(
        related="company_id.sdi_channel_id", string="ES channel", readonly=False
    )
    sdi_channel_type = fields.Selection(
        related="sdi_channel_id.channel_type", readonly=True
    )
