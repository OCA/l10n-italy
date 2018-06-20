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

from openerp.osv import osv, fields
from openerp.tools.translate import _


class MailComposeMessage(osv.TransientModel):
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
        'server_id': _get_def_server,
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
        return super(MailComposeMessage, self).send_mail(
            cr, uid, ids, context=context)

    def get_message_data(self, cr, uid, message_id, context=None):
        if not message_id:
            return {}
        if context is None:
            context = {}
        if context.get('reply_pec'):
            result = super(MailComposeMessage, self).get_message_data(
                cr, uid, message_id, context=context)
            # get partner_ids from action context
            partner_ids = context.get('default_partner_ids', [])
            # update the result
            result.update({
                'partner_ids': partner_ids,
            })
            return result
        else:
            return super(MailComposeMessage, self).get_message_data(
                cr, uid, message_id, context=context)

    def get_record_data(self, cr, uid, values, context=None):
        """ Returns a defaults-like dict with initial values for the
        composition wizard when sending an email related a previous email
        (parent_id) or a document (model, res_id).
        This is based on previously computed default values. """
        if context is None:
            context = {}
        result = super(MailComposeMessage, self).get_record_data(
            cr, uid, values, context=context)
        if 'reply_pec' in context and context['reply_pec']:
            if 'parent_id' in values:
                parent = self.pool.get('mail.message').browse(
                    cr, uid, values.get('parent_id'), context=context)
                result['parent_id'] = parent.id
                subject = parent.subject
                re_prefix = _('Re:')
                if subject and not \
                        (subject.startswith('Re:') or
                         subject.startswith(re_prefix)):
                    subject = "%s %s" % (re_prefix, subject)
                    result['subject'] = subject
        return result
