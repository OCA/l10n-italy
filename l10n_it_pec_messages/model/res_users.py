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
from openerp import models, fields, api


class ResUsers(models.Model):

    _inherit = 'res.users'

    allowed_server_ids = fields.Many2many(
        'fetchmail.server',
        'fetchmail_server_user_rel', 'user_id', 'server_id',
        string='Fetchmail servers allowed to be used')

    @api.cr_uid_ids_context
    def message_post(self, cr, uid, thread_id, body='',
                     subject=None, type='notification',
                     subtype=None, parent_id=False,
                     attachments=None, context=None,
                     content_subtype='html', **kwargs):
        '''
        if pec_type is accettazione and non-accettazione
            link message as reception type in parent message

        if  pec_type is avvenuta-consegna errore-consegna rilevazione-virus
            link message as delivery type in parent message

        if pec_type is error type like:
            non-accettazione errore-consegna rilevazione-virus
            marks parent message with error flag

        '''
        if context is None:
            context = {}
        message_pool = self.pool['mail.message']
        msg_id = super(ResUsers, self).message_post(
            cr, uid, thread_id, body=body, subject=subject, type=type,
            subtype=subtype, parent_id=parent_id, attachments=attachments,
            context=context, content_subtype=content_subtype, **kwargs)
        # If the message is a notification mail than check its status
        if (
            context.get('main_message_id') and
            context.get('pec_type')
        ):
            message_pool.CheckNotificationStatus(
                cr, uid, context['main_message_id'], context=context)
        return msg_id
