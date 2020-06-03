# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
import re
from unidecode import unidecode
import openerp

from datetime import datetime
from lxml import etree

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT

from openerp.addons.base.ir.ir_mail_server import MailDeliveryException

_logger = logging.getLogger(__name__)

RESPONSE_MAIL_REGEX = '[A-Z]{2}[a-zA-Z0-9]{11,16}_[a-zA-Z0-9]{,5}_[A-Z]{2}_' \
                      '[a-zA-Z0-9]{,3}'


class FatturaPAAttachmentOut(orm.Model):
    _inherit = 'fatturapa.attachment.out'

    _defaults = {
        'state': 'ready',
        'last_sdi_response': 'No response yet',
    }

    _columns = {
        'state': fields.selection([
                ('ready', 'Ready to Send'),
                ('sent', 'Sent'),
                ('sender_error', 'Sender Error'),
                ('recipient_error', 'Recipient Error'),
                ('rejected', 'Rejected (PA)'),
                ('validated', 'Delivered'),
            ], string='State'),
        'last_sdi_response': fields.text('Last Response from Exchange System',
                                         readonly=True),
        'sending_date': fields.datetime('Sent date', readonly=True),
        'delivered_date': fields.datetime('Delivered date', readonly=True),
        'sending_user': fields.many2one('res.users', string='Sending user',
                                        readonly=True),
    }

    def reset_to_ready(self, cr, uid, ids, context=None):
        for attachment in self.browse(cr, uid, ids, context=context):
            if attachment.state != 'sender_error':
                raise osv.except_osv(_('UserError'), _(
                    "You can only reset 'sender error' files"))
            attachment.write({'state': 'ready'})

    def _check_fetchmail(self, cr, uid, context=None):
        server_ids = self.pool.get('fetchmail.server').search(cr, uid, [
                ('is_fatturapa_pec', '=', True),
                ('state', '=', 'done')
            ], context=context)
        if not server_ids:
            raise osv.except_osv(
                _('UserError'),
                _("No incoming PEC server found. Please configure it."))

    def send_via_pec(self, cr, uid, ids, context=None):
        self._check_fetchmail(cr, uid, context=context)
        company = self.pool.get('res.users').browse(
            cr, uid, uid, context=context).company_id
        attachments = self.browse(cr, uid, ids, context=context)

        for attachment in attachments:
            if attachment.state != 'ready':
                raise osv.except_osv(
                    _('UserError'),
                    _("You can only send 'ready to send' files"))

        for attachment in attachments:
            mail_message_id = self.pool.get('mail.message').create(cr, uid, {
                'model': self._name,
                'res_id': attachment.id,
                'subject': attachment.name,
                'body': 'XML file for FatturaPA {} sent to Exchange System to '
                        'the email address {}.'
                .format(
                    attachment.name,
                    company.email_exchange_system),
                'attachment_ids': [(6, 0, [
                    a.id for a in (attachment.ir_attachment_id if isinstance(
                        attachment.ir_attachment_id, list) else
                                   [attachment.ir_attachment_id])])],
            }, context=context)

            mail_obj = self.pool.get('mail.mail')
            mail_id = mail_obj.create(cr, uid, {
                'mail_message_id': mail_message_id,
                'body_html': self.pool['mail.message'].browse(
                    cr, uid, mail_message_id, context=context).body,
                'email_to': company.email_exchange_system,
                'email_from': company.email_from_for_fatturaPA,
                'mail_server_id': company.sdi_channel_id.pec_server_id.id,
            })

            if mail_id:
                mail_obj.send(cr, uid, [mail_id], context=context)
                mail = mail_obj.browse(cr, uid, mail_id, context=context)
                if mail.state == 'sent':
                    attachment.write({
                            'state': 'sent',
                            'sending_date': datetime.now().strftime(
                                DEFAULT_SERVER_DATETIME_FORMAT),
                            'sending_user': uid,
                        })
                else:
                    attachment.write({
                            'state': 'sender_error',
                        })
                    mail_obj.write(cr, uid, [mail_id], {
                        'body': 'sender_error'}, context=context)
            return True

    def parse_pec_response(self, cr, uid, message_dict, context=None):
        message_dict['model'] = self._name
        message_dict['res_id'] = 0

        regex = re.compile(RESPONSE_MAIL_REGEX)
        attachments = [a for a in message_dict['attachments']
                       if regex.match(a[0])]

        for attachment in attachments:
            response_name = attachment[0]
            message_type = response_name.split('_')[2]
            if attachment[0].lower().endswith('.zip'):
                # not implemented, case of AT, todo
                continue
            root = etree.fromstring(attachment[1])
            file_name = root.find('NomeFile')
            fatturapa_attachment_out_ids = False

            if file_name is not None:
                file_name = file_name.text
                fatturapa_attachment_out_ids = self.search(cr, uid, [
                        '|',
                        ('datas_fname', '=', file_name),
                        ('datas_fname', '=', file_name.replace('.p7m', '')),
                        ], context=context)
                if len(fatturapa_attachment_out_ids) > 1:
                    _logger.info(
                        'More than 1 out invoice found for incoming message')
                if not fatturapa_attachment_out_ids:
                    if message_type == 'MT':  # Metadati
                        # out invoice not found, so it is an incoming invoice
                        return message_dict
                    else:
                        _logger.info('Error: FatturaPA {} not found.'.format(
                            file_name))
                        # TODO Send a mail warning
                        return message_dict

            if fatturapa_attachment_out_ids:
                fatturapa_attachment_out = self.browse(
                    cr, uid, fatturapa_attachment_out_ids[0], context=context)
                id_sdi = root.find('IdentificativoSdI')
                receipt_dt = root.find('DataOraRicezione')
                message_id = root.find('MessageId')
                id_sdi = id_sdi.text if id_sdi is not None else False
                receipt_dt = receipt_dt.text if receipt_dt is not None else \
                    False
                message_id = message_id.text if message_id is not None else \
                    False
                if message_type == 'NS':  # 2A. Notifica di Scarto
                    error_list = root.find('ListaErrori')
                    error_str = ''
                    for error in error_list:
                        error_str += "\n[%s] %s %s" % (
                            error.find('Codice').text if error.find(
                                'Codice') is not None else '',
                            error.find('Descrizione').text if error.find(
                                'Descrizione') is not None else '',
                            error.find('Suggerimento').text if error.find(
                                'Suggerimento') is not None else ''
                        )
                    fatturapa_attachment_out.write({
                        'state': 'sender_error',
                        'last_sdi_response': 'SdI ID: %r; '
                        'Message ID: %r; Receipt date: %r; '
                        'Error: %r' % (id_sdi, message_id, receipt_dt, error_str)
                    })
                elif message_type == 'MC':  # 3A. Mancata consegna
                    missed_delivery_note = root.find('Descrizione').text
                    missed_delivery_note = unidecode(missed_delivery_note)
                    fatturapa_attachment_out.write({
                        'state': 'recipient_error',
                        'last_sdi_response': 'SdI ID: {}; '
                        'Message ID: {}; Receipt date: {}; '
                        'Missed delivery note: {}'.format(
                            id_sdi, message_id, receipt_dt,
                            missed_delivery_note)
                    })
                elif message_type == 'RC':  # 3B. Ricevuta di Consegna
                    delivery_dt = root.find('DataOraConsegna').text
                    fatturapa_attachment_out.write({
                        'state': 'validated',
                        'delivered_date': datetime.now(),
                        'last_sdi_response': 'SdI ID: {}; '
                        'Message ID: {}; Receipt date: {}; '
                        'Delivery date: {}'.format(
                            id_sdi, message_id, receipt_dt, delivery_dt)
                    })
                elif message_type == 'NE':  # 4A. Notifica Esito per PA
                    esito_committente = root.find('EsitoCommittente')
                    if esito_committente is not None:
                        # more than one esito?
                        esito = esito_committente.find('Esito')
                        if esito is not None:
                            if esito.text == 'EC01':
                                state = 'validated'
                            elif esito.text == 'EC02':
                                state = 'rejected'
                            fatturapa_attachment_out.write({
                                'state': state,
                                'last_sdi_response': 'SdI ID: {}; '
                                'Message ID: {}; Response: {}; '.format(
                                    id_sdi, message_id, esito.text)
                            })
                elif message_type == 'DT':  # 5. Decorrenza Termini per PA
                    description = root.find('Descrizione')
                    if description is not None:
                        fatturapa_attachment_out.write({
                            'state': 'validated',
                            'last_sdi_response': 'SdI ID: {}; '
                            'Message ID: {}; Receipt date: {}; '
                            'Description: {}'.format(
                                id_sdi, message_id, receipt_dt,
                                description.text)
                        })
                # not implemented - todo
                elif message_type == 'AT':  # 6. Avvenuta Trasmissione per PA
                    description = root.find('Descrizione')
                    if description is not None:
                        fatturapa_attachment_out.write({
                            'state': 'validated',
                            'last_sdi_response': (
                                'SdI ID: {}; Message ID: {}; Receipt date: {};'
                                ' Description: {}'
                            ).format(
                                id_sdi, message_id, receipt_dt,
                                description.text)
                        })

                message_dict['res_id'] = fatturapa_attachment_out.id
        return message_dict

    def unlink(self, cr, uid, ids, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        for attachment in self.browse(cr, uid, ids, context=context):
            if attachment.state != 'ready':
                raise osv.except_osv(
                    _('UserError'),
                    _("You can only delete 'ready to send' files"))
        return super(FatturaPAAttachmentOut, self).unlink(
            cr, uid, ids, context=context)
