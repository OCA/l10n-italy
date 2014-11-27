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


class MailMessage(orm.Model):
    _inherit = "mail.message"

    _columns = {
        'server_id': fields.many2one(
            'fetchmail.server', 'Server Pec', readonly=True),
        'pec_type': fields.selection([
            ('posta-certificata', 'Pec Mail'),
            ('accettazione', 'Reception'),
            ('presa-in-carico', 'In Progress'),
            ('avvenuta-consegna', 'Delivery'),
            ('errore-consegna', 'Delivery Error'),
            ('preavviso-errore-consegna', 'Notice Delivery Error'),
            ('rilevazione-virus', 'Virus Detected'),
            ], 'Pec Type', readonly=True),
        'cert_datetime': fields.datetime(
            'Certified Date and Time ', readonly=True),
        'pec_msg_id': fields.char(
            'PEC-Message-Id',
            help='Message unique identifier', select=1, readonly=True),
        'ref_msg_id': fields.char(
            'ref-Message-Id',
            help='Ref Message unique identifier', select=1, readonly=True),
        'delivery_message_id': fields.many2one(
            'mail.message', 'Delivery Message', readonly=True),
        'reception_message_id': fields.many2one(
            'mail.message', 'Reception Message', readonly=True),
        'main_msg_delivery_message_ids': fields.one2many(
            'mail.message', 'delivery_message_id', 'Main messages', readonly=True),
        'main_msg_reception_message_ids': fields.one2many(
            'mail.message', 'reception_message_id', 'Main messages', readonly=True),
    }

    def get_datafrom_daticertxml(self,daticertxml,contex=None):
        ret={}
        content = self.getFile(daticertxml).decode('base64')
        daticert = ElementTree(fromstring(content))

    def _search(
        self, cr, uid, args, offset=0, limit=None, order=None,
        context=None, count=False, access_rights_uid=None
    ):
        if context is None:
            context = {}
        if context.get('pec_messages'):
            return super(orm.Model, self)._search(
                cr, uid, args, offset=offset, limit=limit, order=order,
                context=context, count=count,
                access_rights_uid=access_rights_uid)
        else:
            return super(MailMessage, self)._search(
                cr, uid, args, offset=offset, limit=limit, order=order,
                context=context, count=count,
                access_rights_uid=access_rights_uid)

    def check_access_rule(self, cr, uid, ids, operation, context=None):
        if context is None:
            context = {}
        if context.get('pec_messages'):
            return super(orm.Model, self).check_access_rule(
                cr, uid, ids, operation, context=context)
        else:
            return super(MailMessage, self).check_access_rule(
                cr, uid, ids, operation, context=context)
