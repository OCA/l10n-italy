# Copyright 2018 Sergio Corato (https://efatto.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class SdiChannel(models.Model):
    _name = "sdi.channel"
    _description = "ES channel"

    name = fields.Char(string='Name', required=True)
    company_id = fields.Many2one(
        'res.company', string='Company', required=True,
        default=lambda self:
        self.env['res.company']._company_default_get('sdi.channel'))
    channel_type = fields.Selection(
        string='ES channel type', selection=[], required=True,
        help='Channels (Pec, Web, Sftp) could be provided by external modules.',
    )
