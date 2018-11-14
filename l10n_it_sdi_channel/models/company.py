# -*- coding: utf-8 -*-
# Copyright 2018 Sergio Corato (https://efatto.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    sdi_channel_id = fields.Many2one(
        'sdi.channel',
        string='SdI channel'
    )

    sdi_channel_type = fields.Selection(
        related='sdi_channel_id.channel_type',
        readonly=True
    )

    email_from_for_fatturaPA = fields.Char(
        string='Sender Email Address',
        related='sdi_channel_id.pec_server_id.email_from_for_fatturaPA',
        readonly=True
    )

    email_exchange_system = fields.Char(
        string='Exchange System Email Address',
        related='sdi_channel_id.email_exchange_system',
        readonly=True
    )


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    sdi_channel_id = fields.Many2one(
        related='company_id.sdi_channel_id',
        string='SdI channel'
    )

    sdi_channel_type = fields.Selection(
        related='sdi_channel_id.channel_type',
        readonly=True
    )

    email_from_for_fatturaPA = fields.Char(
        string='Sender Email Address',
        related='sdi_channel_id.pec_server_id.email_from_for_fatturaPA',
        readonly=True
    )

    email_exchange_system = fields.Char(
        string='Exchange System Email Address',
        related='sdi_channel_id.email_exchange_system',
        readonly=True
    )
