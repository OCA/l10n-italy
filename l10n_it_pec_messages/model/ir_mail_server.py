# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Associazione Odoo Italia
#    (<http://www.odoo-italia.org>).
#    Copyright 2014 Agile Business Group http://www.agilebg.com
#    @authors
#       Alessio Gerace <alessio.gerace@gmail.com>
#       Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#       Roberto Onnis <roberto.onnis@innoviu.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################
from openerp.osv import fields, orm


class ir_mail_server(orm.Model):
    """Represents an SMTP server, able to send
        outgoing emails, with SSL and TLS capabilities."""
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
        ('incomingserver_name_unique', 'unique(name,in_server_rel)',
         'Incoming Server already in use'),
        ]
