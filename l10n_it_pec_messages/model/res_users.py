# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class ResUsers(models.Model):

    _inherit = 'res.users'

    allowed_server_ids = fields.Many2many(
        'fetchmail.server',
        'fetchmail_server_user_rel', 'user_id', 'server_id',
        string='Fetchmail servers allowed to be used')
