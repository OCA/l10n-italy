# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2014-2015 Agile Business Group http://www.agilebg.com
#    @authors
#       Alessio Gerace <alessio.gerace@gmail.com>
#       Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#       Roberto Onnis <roberto.onnis@innoviu.com>
#
#   About license see __openerp__.py
#
##############################################################################

from openerp import models, fields


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

    force_create_partner_from_mail = fields.Boolean(
        "Force Create Partner",
        help="If checked then if there is no partner"
             " to link a fetched mail with,"
             "the system creates a contact partner")
