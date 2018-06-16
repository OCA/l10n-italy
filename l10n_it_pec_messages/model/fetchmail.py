# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class FetchmailServer(models.Model):

    _inherit = "fetchmail.server"

    pec = fields.Boolean(
        "Pec Server",
        help="Check if this server is PEC")

    user_ids = fields.Many2many(
        'res.users',
        'fetchmail_server_user_rel', 'server_id', 'user_id',
        string='Users allowed to use this server')

    out_server_id = fields.One2many(
        'ir.mail_server',
        'in_server_id',
        string='Outgoing Server',
        readonly=True,
        copy=False)
