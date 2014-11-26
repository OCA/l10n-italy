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

import email
from openerp import SUPERUSER_ID
from openerp.addons.mail.mail_message import decode
from openerp.osv import orm
from openerp.tools.translate import _
import xml.etree.ElementTree as ET


class mail_thread(orm.Model):
    _inherit = 'mail.thread'

    def is_server_pec(self, cr, uid, context=None):
        if context is None:
            context = {}
        server_pool = self.pool.get('fetchmail.server')
        if 'fetchmail_server_id' in context:
            id = context.get('fetchmail_server_id')
            server = server_pool.read(cr, SUPERUSER_ID, [id], ['pec'])
            return server[0]['pec']
        return False

    def parse_daticert(self, cr, uid, daticert, context=None):
        msg_dict = {}
        root = ET.fromstring(daticert)
        if 'tipo' in root.attrib:
            msg_dict['pec_type'] = root.attrib['tipo']
        return msg_dict

    def message_parse(
        self, cr, uid, message, save_original=False, context=None
    ):
        if not self.is_server_pec(cr, uid, context=context):
            return super(mail_thread, self).message_parse(
                cr, uid, message, save_original=save_original, context=context)
        postacert = False
        daticert = False
        for part in message.walk():
            filename = part.get_param('filename', None, 'content-disposition')
            if not filename:
                filename = part.get_param('name', None)
            if filename:
                if isinstance(filename, tuple):
                    # RFC2231
                    filename = email.utils.collapse_rfc2231_value(
                        filename).strip()
                else:
                    filename = decode(filename)
            if filename == 'postacert.eml' or filename == 'daticert.xml':
                if part.is_multipart() and len(part.get_payload()) > 1:
                    raise orm.except_orm(
                        _('Error'),
                        _("Too many payloads for 'postacert.eml' or "
                          "'daticert.xml'. Not handled"))
                if part.is_multipart():
                    attachment = part.get_payload()[0]
                else:
                    attachment = part.get_payload(decode=True)
                if filename == 'postacert.eml':
                    postacert = attachment
                if filename == 'daticert.xml':
                    daticert = attachment
        import pdb; pdb.set_trace()
        if not postacert:
            raise orm.except_orm(
                _('Error'), _('PEC message does not contain postacert.eml'))
        if not daticert:
            raise orm.except_orm(
                _('Error'), _('PEC message does not contain daticert.xml'))
        msg_dict = super(mail_thread, self).message_parse(
            cr, uid, postacert, save_original=save_original,
            context=context)
        msg_dict.update(self.parse_daticert(
            cr, uid, daticert, context=context))
        return msg_dict
