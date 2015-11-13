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


class ResPartner(orm.Model):

    # inherit partner because PEC mails are not supposed to be associate to
    # generic models
    _inherit = "res.partner"

    def message_post(
        self, cr, uid, thread_id, body='', subject=None, type='notification',
        subtype=None, parent_id=False, attachments=None, context=None,
        content_subtype='html', **kwargs
    ):
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
        msg_id = super(ResPartner, self).message_post(
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

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = []
        if context.get('show_pec_email'):
            for record in self.browse(cr, uid, ids, context=context):
                name = record.name
                if (
                    record.parent_id and not
                    record.is_company
                ):
                    name = "%s, %s" % (record.parent_name, name)
                if record.pec_mail:
                    name = "%s <%s>" % (name, record.pec_mail)
                res.append((record.id, name))
            return res
        else:
            return super(ResPartner, self).name_get(
                cr, uid, ids, context=context)
