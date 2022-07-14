# Copyright 2018 Sergio Corato (https://efatto.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    sdi_channel_id = fields.Many2one(
        'sdi.channel', string='ES channel')
    sdi_channel_type = fields.Selection(
        related='sdi_channel_id.channel_type', readonly=True)
    e_invoice_user_id = fields.Many2one(
        comodel_name="res.users",
        string="E-bill creator",
        help="This user will be used at supplier e-bill creation.",
        default=lambda self: self.env.user.id
    )


class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sdi_channel_id = fields.Many2one(
        related='company_id.sdi_channel_id', string='ES channel',
        readonly=False)
    sdi_channel_type = fields.Selection(
        related='sdi_channel_id.channel_type', readonly=True)
    e_invoice_user_id = fields.Many2one(
        related='company_id.e_invoice_user_id',
        readonly=False,
    )
    group_sdi_channel_validate_send = fields.Boolean(
        string="Validate, export and send invoices",
        help="Allow users to validate, export and send invoices to SdI "
             "in one click.",
        implied_group='l10n_it_sdi_channel.res_groups_validate_send',
    )
