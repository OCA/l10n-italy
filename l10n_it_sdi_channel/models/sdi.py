# Copyright 2018 Sergio Corato (https://efatto.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SdiChannel(models.Model):
    _name = "sdi.channel"
    _description = "ES channel"

    name = fields.Char(required=True, translate=True)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )
    channel_type = fields.Selection(
        string="ES channel type",
        selection=[],
        required=True,
        help="Channels (Pec, Web, Sftp) could be provided by external modules.",
    )
