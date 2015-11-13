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

from openerp.osv import fields, orm


class FetchmailServer(orm.Model):

    _inherit = "fetchmail.server"

    _columns = {
        'pec': fields.boolean(
            "Pec Server",
            help="Check if this server is PEC"),
        'user_ids': fields.many2many(
            'res.users', 'fetchmail_server_user_rel',
            'server_id', 'user_id',
            'Users allowed to use this server'),
        'out_server_id': fields.one2many(
            'ir.mail_server', 'in_server_id',
            'Outgoing Server',  readonly=True),
        'force_create_partner_from_mail': fields.boolean(
            "Force Create Partner",
            help="If checked then if there is no partner"
                 " to link a fetched mail with,"
                 "the system creates a contact partner"),
    }
