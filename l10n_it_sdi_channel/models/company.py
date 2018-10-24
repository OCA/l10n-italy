# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    sdi_channel_id = fields.Many2one(
        'sdi.channel', string='SdI channel')
    email_from_for_fatturaPA = fields.Char(
        string='Sender Email Address for FatturaPA',
        related='sdi_channel_id.email_from_for_fatturaPA', readonly=True)
    email_exchange_system = fields.Char(
        string='Exchange System Email Address',
        related='sdi_channel_id.email_exchange_system', readonly=True)


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    sdi_channel_id = fields.Many2one(
        related='company_id.sdi_channel_id', string='SdI channel')
    email_from_for_fatturaPA = fields.Char(
        string='Sender Email Address for FatturaPA',
        related='sdi_channel_id.email_from_for_fatturaPA', readonly=True)
    email_exchange_system = fields.Char(
        string='Exchange System Email Address',
        related='sdi_channel_id.email_exchange_system', readonly=True)
