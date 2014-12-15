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

    def send_email(
        self, cr, uid, message, mail_server_id=None,
        smtp_server=None, smtp_port=None, smtp_user=None,
        smtp_password=None, smtp_encryption=None,
        smtp_debug=False, context=None
    ):

        if (
            'pec_state' in context and
            context['pec_state'] == 'new'
        ):
            return False
        else:
            if context.get('new_pec_server_id'):
                mail_server_id = context.get('new_pec_server_id')

            return super(ir_mail_server, self).send_email(
                cr, uid, message, mail_server_id=mail_server_id,
                smtp_server=smtp_server, smtp_port=smtp_port,
                smtp_user=smtp_user, smtp_password=smtp_password,
                smtp_encryption=smtp_encryption, smtp_debug=smtp_debug,
                context=context)
