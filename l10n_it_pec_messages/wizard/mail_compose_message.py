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
from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _


class mail_compose_message(osv.TransientModel):
    _inherit = 'mail.compose.message'

    def _get_def_server(self, cr, uid, context=None):
        res = self.pool.get('fetchmail.server').search(
            cr, uid, [('user_ids', 'in', uid)], context=context)
        return res and res[0] or False

    _columns = {
        'server_id': fields.many2one(
            'fetchmail.server', 'Server', required=True),
    }
    _defaults = {
        'server_id': _get_def_server
    }

    def send_mail(self, cr, uid, ids, context=None):
        """ Override of send_mail to duplicate attachments linked to the
        email.template.
            Indeed, basic mail.compose.message wizard duplicates attachments
            in mass
            mailing mode. But in 'single post' mode, attachments of an
            email template
            also have to be duplicated to avoid changing their ownership. """
        for wizard in self.browse(cr, uid, ids, context=context):
            if context.get('new_pec_mail'):
                context['new_pec_server_id'] = wizard.server_id.id
                for partner in wizard.partner_ids:
                    if not partner.pec_mail:
                        raise osv.except_osv(
                            _('Error'),
                            _('No PEC mail for partner %s') % partner.name)
        return super(mail_compose_message, self).send_mail(
            cr, uid, ids, context=context)

    def get_message_data(self, cr, uid, message_id, context=None):
        if not message_id:
            return {}
        if context is None:
            context = {}
        if context.get('reply_pec'):
            message_data = self.pool.get('mail.message').browse(cr, uid, message_id, context=context)

            # create subject
            re_prefix = _('Re:')
            reply_subject = tools.ustr(message_data.subject or message_data.record_name or '')
            if not (reply_subject.startswith('Re:') or reply_subject.startswith(re_prefix)) and message_data.subject:
                reply_subject = "%s %s" % (re_prefix, reply_subject)
            # get partner_ids from action context
            partner_ids = context.get('default_partner_ids', [])

            # update the result
            result = {
                'record_name': message_data.record_name,
                'model': message_data.model,
                'res_id': message_data.res_id,
                'parent_id': message_data.id,
                'subject': reply_subject,
                'partner_ids': partner_ids,
            }
            return result
        else:
            return super(mail_compose_message, self).get_message_data(
                cr, uid, message_id, context=context)