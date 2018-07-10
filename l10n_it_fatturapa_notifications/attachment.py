# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
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
#
##############################################################################

from openerp.osv import fields, orm
import base64
import re


class FatturaPANotification(orm.Model):
    _name = "fatturapa.notification"
    _description = "FatturaPA Notification"
    _inherits = {'ir.attachment': 'ir_attachment_id'}

    def _get_file_identifier(
        self, cr, uid, ids, field_name, arg, context=None
    ):
        res = {}
        for notification in self.browse(cr, uid, ids, context=context):
            res[notification.id] = self.get_file_identifier(
                notification.datas_fname)
        return res

    _columns = {
        'ir_attachment_id': fields.many2one(
            'ir.attachment', 'Attachment', required=True, ondelete="cascade"),
        'message_type': fields.selection([
            ('RC', 'Ricevuta di consegna'),
            ('NS', 'Notifica di scarto'),
            ('MC', 'Notifica di mancata consegna'),
            ('NE', 'Notifica esito cedente / prestatore'),
            ('MT', 'File dei metadati'),
            ('EC', 'Notifica di esito cessionario / committente'),
            ('SE', 'Notifica di scarto esito cessionario / committente'),
            ('DT', 'Notifica decorrenza termini'),
            ('AT', 'Attestazione di avvenuta trasmissione della fattura con '
                   'impossibilità di recapito'),
        ], string="Message Type",
            help="Page 32 of http://www.fatturapa.gov.it/export/fatturazione/"
                 "sdi/Specifiche_tecniche_SdI_v1.1.pdf ",
            readonly=True),
        'sequence': fields.char(
            "Sequence", size=3,
            help="It must be an alphanumeric string with a maximum length of 3"
                 " characters and allowed values [a - z], [A - Z], [0-9] which"
                 " uniquely identifies each notification / receipt for the "
                 "sent file",
            readonly=True),
        'file_identifier': fields.function(
            _get_file_identifier, type="char", size=512,
            string="File identifier", store=True),  # is store=True enough?
    }

    def save_notification_xml(
        self, cr, uid, ids, xml, file_name, invoice_type="supplier",
        context=None
    ):
        """
        IT accepts an XML string and creates a related 'fatturapa.notification'
        record
        file_name must be in the form IT01234567890_11111_MT_001.xml
        invoice_type is used by derived modules
        Returns new record ID
        """
        identifier = self.get_file_identifier(file_name)
        if context is None:
            context = {}
        mtype, sequence = identifier.split("_")[2:]
        res_id = self.create(cr, uid, {
            'name': file_name,
            'datas_fname': file_name,
            'datas': base64.encodestring(xml),
            'message_type': mtype,
            'sequence': sequence,
        }, context=context)
        return res_id

    def get_file_identifier(self, file_name):
        """
        Accepts file name and produces file identifier, without file extension
        See 2.2 at
http://www.fatturapa.gov.it/export/fatturazione/sdi/Specifiche_tecniche_SdI_v1.1.pdf
        """
        insensitive_xml_p7m = re.compile(
            re.escape('.xml.p7m'), re.IGNORECASE)
        file_name = insensitive_xml_p7m.sub('', file_name)
        insensitive_xml_p7m = re.compile(
            re.escape('.xml'), re.IGNORECASE)
        file_name = insensitive_xml_p7m.sub('', file_name)
        insensitive_xml_p7m = re.compile(
            re.escape('.zip'), re.IGNORECASE)
        file_name = insensitive_xml_p7m.sub('', file_name)
        return file_name
