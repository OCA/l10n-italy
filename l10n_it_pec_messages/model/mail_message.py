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


class PecNotifications(orm.Model):
    _name = "pec.notifications"
    _order = 'name'
    _columns = {
        'parent_id': fields.many2one(
            'mail.message', 'Main messages', select=True,
            ondelete='set null', help="Related Message."),
        'name': fields.many2one(
            'mail.message', 'Notification Message', select=True,
            ondelete='set null', help="Notification Message."),
        'recipient': fields.related(
            'name', 'recipient_id',
            type='many2one',
            relation='res.partner',
            string="Recipient", readonly=True,
        ),
        'recipient_addr': fields.related(
            'name', 'recipient_id', 'pec_mail',
            type='char',
            string="Recipient Address", readonly=True,
        ),
        'type': fields.related(
            'name', 'pec_type',
            type='char',
            string="Notice Type", readonly=True,
        ),
        'error': fields.related(
            'name', 'err_type',
            type='char',
            string="Error", readonly=True,
        ),
    }


class MailMessage(orm.Model):
    _inherit = "mail.message"

    def _get_out_server(self, cr, uid, ids, name,
                        args, context=None):
        res = {}
        if not context:
            context = {}
        for id in self.browse(cr, uid, ids, context=context):
            res[id.id] = False
            if id.server_id:
                if id.server_id.out_server_id:
                    res[id.id] = id.server_id.out_server_id[0].id
        return res

    _columns = {
        'server_id': fields.many2one(
            'fetchmail.server', 'Server Pec', readonly=True),
        'out_server_id': fields.function(
            _get_out_server, type='many2one',
            relation='ir.mail_server',
            string='Related Outgoing Server'),
        'direction': fields.selection([
            ('in', 'in'),
            ('out', 'out'),
            ], 'Mail direction'),
        'pec_type': fields.selection([
            ('posta-certificata', 'Pec Mail'),
            ('accettazione', 'Reception'),
            ('non-accettazione', 'No Reception'),
            ('presa-in-carico', 'In Progress'),
            ('avvenuta-consegna', 'Delivery'),
            ('errore-consegna', 'Delivery Error'),
            ('preavviso-errore-consegna', 'Notice Delivery Error'),
            ('rilevazione-virus', 'Virus Detected'),
            ], 'Pec Type', readonly=True),
        'error': fields.boolean('Reception Delivery Error'),
        'err_type': fields.selection([
            ('nessuno', 'No Error'),
            ('no-dest', 'Recipient Adress Error'),
            ('no-dominio', 'Recipient domain Error'),
            ('virus', 'Virus Detected Error'),
            ('altro', 'Undefined Error'),
            ], 'Pec Error Type', readonly=True),
        'cert_datetime': fields.datetime(
            'Certified Date and Time ', readonly=True),
        'pec_msg_id': fields.char(
            'PEC-Message-Id',
            help='Message unique identifier', select=1, readonly=True),
        'ref_msg_id': fields.char(
            'ref-Message-Id',
            help='Ref Message unique identifier', select=1, readonly=True),

        'recipient_id': fields.many2one(
            'res.partner', 'Recipient', readonly=True),

        'reception_message_id': fields.many2one(
            'mail.message', 'Reception Message', readonly=True),

        'no_reception_message_id': fields.many2one(
            'mail.message', 'No Reception Message', readonly=True),

        'pec_notifications_ids': fields.one2many(
            'pec.notifications', 'parent_id',
            'Related Notifications',  readonly=True),
        # TODO
        # delete delete follow fields when
        # new implementations are tested
        'inprogress_message_id': fields.many2one(
            'mail.message', 'Message In Progress', readonly=True),

        'notice_delivery_err_message_id': fields.many2one(
            'mail.message', 'Notice Error Delivery Message', readonly=True),
        'delivery_message_id': fields.many2one(
            'mail.message', 'Delivery Message', readonly=True),
        'delivery_err_message_id': fields.many2one(
            'mail.message', 'Error Delivery Message', readonly=True),
        'virus_message_id': fields.many2one(
            'mail.message', 'Virus Detected', readonly=True),


        'main_msg_progress_message_ids': fields.one2many(
            'mail.message', 'inprogress_message_id',
            'Main messages',  readonly=True),
        'main_msg_delivery_message_ids': fields.one2many(
            'mail.message', 'delivery_message_id',
            'Main messages',  readonly=True),
        'main_msg_delivery_err_message_ids': fields.one2many(
            'mail.message', 'delivery_err_message_id',
            'Main messages',  readonly=True),
        'main_msg_notice_delivery_err_message_ids': fields.one2many(
            'mail.message', 'notice_delivery_err_message_id',
            'Main messages',  readonly=True),
        'main_msg_reception_message_ids': fields.one2many(
            'mail.message', 'reception_message_id',
            'Main messages', readonly=True),
        'main_msg_no_reception_message_ids': fields.one2many(
            'mail.message', 'no_reception_message_id',
            'Main messages', readonly=True),
        'main_msg_virus_message_ids': fields.one2many(
            'mail.message', 'virus_message_id',
            'Main messages', readonly=True),
    }

    _defaults = {
        'direction': 'in'
    }

    def CheckStatus(self, cr, uid, ids, context=None):
        notif_pool = self.pool['pec.notifications']
        if context is None:
            context = {}
        if not hasattr(ids, '__iter__'):
            ids = [ids]
        error_lst = []
        noerror_lst = ids
        if ids:
            for message in self.bmessagese(cr, uid, ids, context=context):
                if message.reception_message_id is False:
                    error_lst.append(message.id)
                else:
                    for partner in message.partner_ids:
                        if message.id not in error_lst:
                            existid = notif_pool.search(
                                cr, uid,
                                [
                                    ('parent_id', '=', message.id),
                                    ('recipient', '=', partner.id)
                                ],
                                context=context
                            )
                            if not existid:
                                error_lst.append(message.id)
                            else:
                                errors = notif_pool.search(
                                    cr, uid,
                                    [
                                        ('id', 'in', existid),
                                        ('error', '!=', 'nessuno')
                                    ],
                                    context=context
                                )
                                if errors:
                                    error_lst.append(message.id)
                                deliveries = notif_pool.search(
                                    cr, uid,
                                    [
                                        ('id', 'in', existid),
                                        ('type', '=', 'avvenuta-consegna')
                                    ],
                                    context=context
                                )
                                if not deliveries:
                                    error_lst.append(message.id)
        if error_lst:
            self.write(cr, uid, error_lst, {'error': True}, context=context)
            noerror_lst = [item for item in ids if item not in error_lst]
        if noerror_lst:
            self.write(cr, uid, noerror_lst, {'error': False}, context=context)
        return True

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
