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
from openerp.tools.translate import _
import base64


class FatturaPANotification(orm.Model):
    _name = "fatturapa.notification"
    _description = "FatturaPA Notification"
    _inherits = {'ir.attachment': 'ir_attachment_id'}

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
        'sequence': fields.integer(
            "Sequence",
            help="It must be an alphanumeric string with a maximum length of 3"
                 " characters and allowed values [a - z], [A - Z], [0-9] which"
                 " uniquely identifies each notification / receipt for the "
                 "sent file",
            readonly=True),
        'fatturapa_attachment_id': fields.many2one(
            'ir.attachment', 'FatturaPA', readonly=True),
        }

    def parse_xml(self, cr, uid, ids, xml, file_name, context=None):
        """
        IT accepts an XML string and creates a related 'fatturapa.notification'
        record
        Returns new record ID
        """
        if context is None:
            context = {}
        attach_pool = self.pool['ir.attachment']
        short_f_name = file_name.replace(".xml", "")
        fattPA, fattPA_seq, mtype, sequence = short_f_name.split("_")
        fattPAname = fattPA + fattPA_seq
        fattPAnameXML = fattPAname + '.xml'
        fattPAnameP7M = fattPAname + '.xml.p7m'
        fattPAnameZIP = fattPAname + '.zip'
        attach_ids = attach_pool.search(cr, uid, [
            '|',
            ('datas_fname', '=', fattPAnameXML),
            '|',
            ('datas_fname', '=', fattPAnameP7M),
            ('datas_fname', '=', fattPAnameZIP),
            ], context=context)
        if not attach_ids:
            raise orm.except_orm(
                _("Error"), _("No fatturaPA files found: %s") % fattPAname)
        if len(attach_ids) > 1:
            raise orm.except_orm(
                _("Error"),
                _("Too many fatturaPA files found: %s") % fattPAname)
        res_id = self.create(cr, uid, {
            'name': file_name,
            'datas_fname': file_name,
            'datas': base64.encodestring(xml),
            'message_type': mtype,
            'sequence': sequence,
            'fatturapa_attachment_id': attach_ids[0],
            }, context=context)
        return res_id
