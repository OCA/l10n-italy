# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api
import base64
import re


class FatturaPANotification(models.Model):
    _name = "fatturapa.notification"
    _description = "FatturaPA Notification"
    _inherits = {'ir.attachment': 'ir_attachment_id'}

    @api.multi
    @api.depends('datas_fname')
    def _get_file_identifier(self):
        for notification in self:
            notification.file_identifier = self.get_file_identifier(
                notification.datas_fname)

    ir_attachment_id = fields.Many2one(
        'ir.attachment', 'Attachment', required=True, ondelete="cascade")
    message_type = fields.Selection([
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
        readonly=True)
    sequence = fields.Char(
        "Sequence",
        help="It must be an alphanumeric string with a maximum length of 3"
             " characters and allowed values [a - z], [A - Z], [0-9] which"
             " uniquely identifies each notification / receipt for the "
             "sent file",
        readonly=True)
    file_identifier = fields.Char(
        compute="_get_file_identifier",
        string="File identifier", store=True)

    def save_notification_xml(self, xml, file_name, invoice_type="supplier"):
        """
        IT accepts an XML string and creates a related 'fatturapa.notification'
        record
        file_name must be in the form IT01234567890_11111_MT_001.xml
        invoice_type is used by derived modules
        Returns new record ID
        """
        identifier = self.get_file_identifier(file_name)
        mtype, sequence = identifier.split("_")[2:]
        res_id = self.create({
            'name': file_name,
            'datas_fname': file_name,
            'datas': base64.encodestring(xml),
            'message_type': mtype,
            'sequence': sequence,
        }).id
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
