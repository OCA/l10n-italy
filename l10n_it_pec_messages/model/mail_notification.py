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

from openerp.osv import orm


class MailNotification(orm.Model):
    _inherit = "mail.notification"

    def get_partners_to_notify(
        self, cr, uid, message, partners_to_notify=None, context=None
    ):
        """
        this allows to send PEC mail to partners without standard email
        """
        notify_pids = super(MailNotification, self).get_partners_to_notify(
            cr, uid, message, partners_to_notify=partners_to_notify,
            context=context)
        if (
            (message.server_id and message.server_id.pec)
            or
            (message.parent_id and message.parent_id.server_id and
            message.parent_id.server_id.pec)
            or
            context.get('new_pec_mail')
        ):
            for notification in message.notification_ids:
                if notification.read:
                    continue
                partner = notification.partner_id
                # If partners_to_notify specified: restrict to them
                if (
                    partners_to_notify is not None
                    and partner.id not in partners_to_notify
                ):
                    continue
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
                # Partner does not want to receive any emails or is opt-out
                if partner.notification_email_send == 'none':
                    continue
                # Partner wants to receive only emails and comments
                if (
                    partner.notification_email_send == 'comment'
                    and message.type not in ('email', 'comment')
                ):
                    continue
                # Partner wants to receive only emails
                if (
                    partner.notification_email_send == 'email'
                    and message.type != 'email'
                ):
                    continue
                notify_pids.append(partner.id)
        return notify_pids
