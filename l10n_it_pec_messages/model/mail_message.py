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
from email.utils import getaddresses

import logging

_logger = logging.getLogger(__name__)


class MailMessage(orm.Model):
    _inherit = "mail.message"

    def _get_out_server(self, cr, uid, ids, name,
                        args, context=None):
        res = {}
        if not context:
            context = {}
        for msg in self.browse(cr, uid, ids, context=context):
            res[msg.id] = False
            if msg.server_id:
                if msg.server_id.out_server_id:
                    res[msg.id] = msg.server_id.out_server_id[0].id
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
        'recipient_addr': fields.char(
            'Recipient Address', size=256, readonly=True),

        'pec_msg_parent_id': fields.many2one(
            'mail.message', 'Parent Message', readonly=True),
        'pec_notifications_ids': fields.one2many(
            'mail.message', 'pec_msg_parent_id',
            'Related Notifications',  readonly=True),
        'message_ok': fields.boolean(
            'Message OK',
            help="System sets this field to True when both delivery and "
                 "reception messages are received for this message"),
        # TODO
        # delete delete follow fields when
        # new implementations are tested
        'reception_message_id': fields.many2one(
            'mail.message', 'Reception Message', readonly=True),

        'no_reception_message_id': fields.many2one(
            'mail.message', 'No Reception Message', readonly=True),

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

    def CheckNotificationStatus(self, cr, uid, ids, context=None):
        mail_mail_pool = self.pool['mail.mail']
        if context is None:
            context = {}
        if not hasattr(ids, '__iter__'):
            ids = [ids]
        error_lst = []
        receipt_list = []
        completed = True
        res = {}
        if ids:
            for message in self.browse(cr, uid, ids, context=context):
                mail_sent_ids = mail_mail_pool.search(
                    cr,
                    uid,
                    [('mail_message_id', '=', message.id)],
                    context=context
                )
                if not mail_sent_ids:
                    _logger.error(
                        'No sent mail for message %s \
                        from %s server %s.', message.id)
                    error_lst.append(message.id)
                elif len(mail_sent_ids) > 1:
                    _logger.error(
                        'Too many sent mails for message %s \
                        from %s server %s.', message.id)
                    error_lst.append(message.id)
                else:
                    sent_mail = mail_mail_pool.browse(
                        cr,
                        uid,
                        mail_sent_ids[0],
                        context=context)
                    receipt_list = [r[1] for r
                                    in getaddresses(
                                        [sent_mail.email_to.lower()]
                                        )
                                    ]
                    res = {receipt: False for receipt in receipt_list}
                    res['accettazione'] = False
                    for notification in message.pec_notifications_ids:
                        if notification.err_type != 'nessuno':
                            error_lst.extend([message.id, notification.id])
                        else:
                            if notification.pec_type == 'accettazione':
                                res['accettazione'] = True
                            elif notification.pec_type == 'avvenuta-consegna':
                                raddress = notification.recipient_addr.lower()
                                if raddress in res:
                                    res[raddress] = True
                            else:
                                pass
                    for value in res.itervalues():
                        completed = completed and value
                    if completed:
                        self.write(cr,
                                   uid,
                                   message.id,
                                   {'message_ok': completed},
                                   context=context
                                   )
        if error_lst:
            self.write(cr, uid, error_lst, {'error': True}, context=context)
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
