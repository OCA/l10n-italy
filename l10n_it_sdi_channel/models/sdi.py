# -*- coding: utf-8 -*-
# Copyright 2018 Sergio Corato (https://efatto.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _, exceptions

SDI_CHANNELS = [
    ('pec', 'PEC'),
    ('web', 'Web service'),
    # ('sftp', 'SFTP'), # not implemented
]


class SdiChannel(models.Model):
    _name = "sdi.channel"
    _description = "SdI channel"

    name = fields.Char(string='Name', required=True)
    company_id = fields.Many2one(
        'res.company', string='Company', required=True,
        default=lambda self:
        self.env['res.company']._company_default_get('sdi.channel'))
    channel_type = fields.Selection(
        string='SdI channel type', selection=SDI_CHANNELS, required=True)
    pec_server_id = fields.Many2one(
        'ir.mail_server', string='Pec mail server', required=False,
        domain=[('is_pec', '=', True)])
    email_from_for_fatturaPA = fields.Char(
        "Sender Email Address for FatturaPA")
    email_exchange_system = fields.Char("Exchange System Email Address")
    web_server_address = fields.Char(string='Web server address')
    web_server_login = fields.Char(string='Web server login')
    web_server_password = fields.Char(string='Web server password')
    web_server_token = fields.Char(string='Web server token')

    @api.constrains('pec_server_id')
    def check_pec_server_id(self):
        for channel in self:
            domain = [('pec_server_id', '=', channel.pec_server_id.id)]
            elements = self.search(domain)
            if len(elements) > 1:
                raise exceptions.ValidationError(
                    _("The channel %s with pec server %s already exists")
                    % (channel.name, channel.pec_server_id.name))
