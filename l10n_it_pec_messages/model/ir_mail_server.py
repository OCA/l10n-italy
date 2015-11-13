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


class ir_mail_server(orm.Model):
    _inherit = "ir.mail_server"

    _columns = {
        'in_server_id':  fields.many2one(
            'fetchmail.server', 'Incoming PEC server',
            domain=[('pec', '=', True)]),
        'pec': fields.boolean(
            "Pec Server",
            help="Check if this server is PEC"),
    }
    _sql_constraints = [
        ('incomingserver_name_unique', 'unique(in_server_id)',
         'Incoming Server already in use'),
        ]
