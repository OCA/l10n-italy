# -*- coding: utf-8 -*-
# Author(s): Andrea Colangelo (andreacolangelo@openforce.it)
# Copyright © 2018 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
import re

from lxml import etree

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

RESPONSE_MAIL_REGEX = '[A-Z]{2}[a-zA-Z0-9]{11,16}_[a-zA-Z0-9]{,5}_[A-Z]{2}_' \
                      '[a-zA-Z0-9]{,3}'


class FatturaPAAttachmentOut(models.Model):
    _inherit = 'fatturapa.attachment.out'

    state = fields.Selection([('ready', 'Ready to Send'),
                              ('sent', 'Sent'),
                              ('validated', 'Validated'),
                              ('sender_error', 'Sender Error'),
                              ('recipient_error', 'Recipient Error')],
                             string='State',
                             default='ready',)

    last_sdi_response = fields.Text(
        string='Last Response from Exchange System', default='No response yet')

    @api.multi
    def send_via_pec(self):

        mail_message = self.env['mail.message'].create({
            'model': self._name,
            'res_id': self.id,
            'subject': self.name,
            'body': 'XML file for FatturaPA {} sent to Exchange System to the'
                    ' email address {}.'
            .format(
                self.name,
                self.env.user.company_id.email_exchange_system),
            'attachment_ids': [(6, 0, [self.ir_attachment_id.id])],
            'email_from': self.env.user.company_id.email_from_for_fatturaPA,
            'mail_server_id': self.env.user.company_id.sdi_channel_id.
            pec_server_id.id,
        })

        self.env['mail.mail'].create({
            'mail_message_id': mail_message.id,
            'body_html': mail_message.body,
            'email_to': self.env.user.company_id.email_exchange_system,
        }).send()
        # TODO Should we disable some mail.* config params before
        # TODO sending? See: https://tinyurl.com/ybr45fxd

        self.state = 'sent'

    @api.multi
    def parse_pec_response(self, message_dict):
        message_dict['model'] = self._name
        message_dict['res_id'] = 0

        regex = re.compile(RESPONSE_MAIL_REGEX)
        for attachment in message_dict['attachments']:
            if regex.match(attachment.fname):
                break

        response_name = attachment.fname
        message_type = response_name.split('_')[2]
        if message_type == 'MT':  # Metadati
            # todo  check if it is only an incoming invoice
            return message_dict, message_type

        root = etree.fromstring(attachment.content)
        file_name = root.find('NomeFile').text

        fatturapa = self.search([('datas_fname', '=', file_name)])
        if not fatturapa:
            _logger.info('Error: FatturaPA {} not found.'.format(file_name))
            # TODO Send a mail warning
            return message_dict, message_type

        id_sdi = root.find('IdentificativoSdI').text
        receipt_dt = root.find('DataOraRicezione').text
        message_id = root.find('MessageId').text
        if message_type == 'RC':  # Ricevuta di Consegna
            delivery_dt = root.find('DataOraConsegna').text
            fatturapa.write({
                'state': 'validated',
                'last_sdi_response': 'SdI ID: {id_sdi}; '
                'Message ID: {message_id}; Receipt date: {receipt_dt}; '
                'Delivery date: {delivery_dt}'.format(
                    id_sdi, message_id, receipt_dt, delivery_dt)
            })
        elif message_type == 'NS':  # Notifica di Scarto
            error_list = root.find('ListaErrori').text
            fatturapa.write({
                'state': 'sender_error',
                'last_sdi_response': 'SdI ID: {id_sdi}; '
                'Message ID: {message_id}; Receipt date: {receipt_dt}; '
                'Error: {error_list}'.format(
                    id_sdi, message_id, receipt_dt, error_list)
            })
        elif message_type == 'MC':  # Mancata consegna
            missed_delivery_note = root.find('Descrizione').text
            fatturapa.write({
                'state': 'recipient_error',
                'last_sdi_response': 'SdI ID: {id_sdi}; '
                'Message ID: {message_id}; Receipt date: {receipt_dt}; '
                'Missed delivery note: {missed_delivery_note}'.format(
                    id_sdi, message_id, receipt_dt, missed_delivery_note)
            })

        message_dict['res_id'] = fatturapa.id
        return message_dict, message_type
