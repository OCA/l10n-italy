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

from openerp.osv import orm
from email.utils import formataddr
from openerp import SUPERUSER_ID
from email.utils import COMMASPACE


class MailMail(orm.Model):
    _inherit = "mail.mail"

    def create(self, cr, uid, values, context=None):
        """
        when replying to a PEC message, or sending a new PEC message,
        use the linked SMTP server and SMTP user
        """
        mail_msg_pool = self.pool.get('mail.message')
        if context.get('new_pec_server_id'):
            values['type'] = 'email'
        res = super(MailMail, self).create(cr, uid, values, context=context)
        mail = self.browse(cr, uid, res, context=context)
        if (
            (
                mail.parent_id and mail.parent_id.server_id and
                mail.parent_id.server_id.pec) or

            context.get('new_pec_server_id')
        ):
            in_server_id = context.get(
                'new_pec_server_id'
            ) or mail.parent_id.server_id.id
            server_pool = self.pool['ir.mail_server']
            server_ids = server_pool.search(
                cr, uid, [('in_server_id', '=', in_server_id)],
                context=context)
            if server_ids:
                server = server_pool.browse(
                    cr, uid, server_ids[0], context=context)
                mail.write({
                    'email_from': server.smtp_user,
                    'mail_server_id': server.id,
                    'server_id': in_server_id,
                    'out_server_id': server.id,
                    'pec_type': 'posta-certificata',
                    'direction': 'out'
                }, context=context)
                mail_msg_pool.write(
                    cr, uid, mail.mail_message_id.id,
                    {'email_from': server.smtp_user})
        return res

    def send_get_email_dict(self, cr, uid, mail, partner=None, context=None):
        res = super(MailMail, self).send_get_email_dict(
            cr, uid, mail, partner=partner, context=context)
        if mail.mail_server_id.pec and partner:
            email_to = [formataddr((partner.name, partner.pec_mail))]
            res['email_to'] = email_to
        return res

    def send(
        self, cr, uid, ids, auto_commit=False, recipient_ids=None, context=None
    ):
        for mail in self.browse(cr, uid, ids, context=context):
            if mail.mail_server_id.pec and recipient_ids:
                # remove duplicate id if there are
                recipient_ids = sorted(set(recipient_ids))
                if recipient_ids:
                    address_lst = ''
                    # save old value of email_to
                    if mail.email_to:
                        address_lst = mail.email_to
                    partner_obj = self.pool.get('res.partner')
                    existing_recipient_ids = partner_obj.exists(
                        cr, SUPERUSER_ID, recipient_ids, context=context)
                    for partner in partner_obj.browse(
                        cr, SUPERUSER_ID, existing_recipient_ids,
                        context=context
                    ):
                        if address_lst:
                            address_lst += COMMASPACE
                        address_lst += formataddr(
                            (partner.name, partner.pec_mail))
                    self.write(
                        cr, uid, mail.id,
                        {'email_to': address_lst}, context=context
                    )
                    recipient_ids = False
        return super(MailMail, self).send(
            cr, uid, ids, auto_commit=auto_commit,
            recipient_ids=recipient_ids, context=context
        )
