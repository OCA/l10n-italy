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


class MailNotification(orm.Model):
    _inherit = "mail.notification"

    def get_partners_to_email(self, cr, uid, ids, message, context=None):
        """
        this allows to send PEC mail to partners without standard email
        """
        notify_pids = super(MailNotification, self).get_partners_to_email(
            cr, uid, ids, message, context=context)
        if (
            (message.server_id and message.server_id.pec) or

            (
                message.parent_id and message.parent_id.server_id and
                message.parent_id.server_id.pec) or

            context.get('new_pec_mail')
        ):
            for notification in message.notification_ids:
                if notification.is_read:
                    continue
                partner = notification.partner_id
                # Do not send to partners without email address defined
                if not partner.pec_mail:
                    continue
                # Do not send to partners having same email address than the
                # author (can cause loops or bounce effect due to messy
                # database)
                if (
                    message.author_id and
                    message.author_id.email == partner.email
                ):
                    continue
                if partner.id not in notify_pids:
                    notify_pids.append(partner.id)
        return notify_pids
