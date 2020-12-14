# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 AgileBG SAGL <http://www.agilebg.com>
#    Copyright (C) 2015 innoviu Srl <http://www.innoviu.com>
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

import base64
from openerp.osv import fields, orm
from openerp.tools.translate import _


class FatturaPAAttachmentIn(orm.Model):
    _name = "fatturapa.attachment.in"
    _description = "FatturaPA import File"
    _inherits = {'ir.attachment': 'ir_attachment_id'}
    _inherit = ['mail.thread']
    _order = 'id desc'

    def _compute_xml_data(self, cr, uid, ids, name, unknow_none, context={}):
        ret = {}
        for att in self.browse(cr, uid, ids, context):
            fatt = self.pool.get('wizard.import.fatturapa').get_invoice_obj(cr, uid, att)
            cedentePrestatore = fatt.FatturaElettronicaHeader.CedentePrestatore
            partner_id = self.pool.get('wizard.import.fatturapa').getCedPrest(
                cr, uid,
                cedentePrestatore)
            vals = {
                'xml_supplier_id': partner_id,
                'invoices_number': len(fatt.FatturaElettronicaBody),
                'invoices_total': 0,
                }
            invoices_total = 0
            for invoice_body in fatt.FatturaElettronicaBody:
                invoices_total += float(
                    invoice_body.DatiGenerali.DatiGeneraliDocumento.ImportoTotaleDocumento or 0
                )
            vals['invoices_total'] = invoices_total            
            ret[att.id] = vals.get(name, False)
        return ret

    def _search_is_registered(self, cr, uid, obj, name, args, context=None):
        operator = 'not in'
        domain = [('in_invoice_ids', '!=', False)]
        ids = self.search(cr, uid, domain, context=context)
        res = []
        for att in self.browse(cr, uid, ids, context):
            if len(att.in_invoice_ids) == att.invoices_number:
                res.append(att.id)
        return [('id', operator, res)]

    def _compute_registered(self, cr, uid, ids, name, unknow_none, context=None):
        ret = {}
        for att in self.browse(cr, uid, ids, context):
            if att.in_invoice_ids and len(att.in_invoice_ids) == att.invoices_number:
                ret[att.id] = True
            else:
                ret[att.id] = False
        return ret

    _columns = {
        'ir_attachment_id': fields.many2one(
            'ir.attachment', 'Attachment', required=True, ondelete="cascade"),
        'in_invoice_ids': fields.one2many(
            'account.invoice', 'fatturapa_attachment_in_id',
            string="In Invoices", readonly=True),
        'xml_supplier_id': fields.function(_compute_xml_data, 
                                           method=True, 
                                           string="Supplier", 
                                           relation="res.partner",
                                           type="many2one",
                                           store=True,),
        'invoices_number': fields.function(_compute_xml_data, 
                                           method=True, 
                                           string="Invoices number", 
                                           type="integer",
                                           store=True,),
        'invoices_total': fields.function(_compute_xml_data, 
                                          method=True,
                                          string="Invoices total",
                                          type="float",
                                          store=True,
                                          help="Se indicato dal fornitore, Importo totale del documento al "
                 "netto dell'eventuale sconto e comprensivo di imposta a debito "
                 "del cessionario / committente"),
        'registered': fields.function(_compute_registered,
            string="Registered", type="boolean", fnct_search=_search_is_registered, store=False),

    'e_invoice_received_date': fields.datetime(string='E-Bill Received Date'),

    'e_invoice_validation_error': fields.boolean(
        compute='_compute_e_invoice_validation_error'),

    'e_invoice_validation_message': fields.text(
        compute='_compute_e_invoice_validation_error'),

    }

    def _compute_e_invoice_validation_error(self, cr, uid, ids, context={}):
        for att in self.browse(cr, uid, ids, context):
            bills_with_error = att.in_invoice_ids.filtered(
                lambda b: b.e_invoice_validation_error
            )
            if not bills_with_error:
                continue
            att.e_invoice_validation_error = True
            errors_message_template = u"{bill}:\n{errors}"
            error_messages = list()
            for bill in bills_with_error:
                error_messages.append(
                    errors_message_template.format(
                        bill=bill.display_name,
                        errors=bill.e_invoice_validation_message))
            att.e_invoice_validation_message = "\n\n".join(error_messages)

    def get_xml_string(self, cr, uid, ids, context={}):
        for fattAttInBrws in self.browse(cr, uid, ids, context):
            return fattAttInBrws.ir_attachment_id.get_xml_string(cr, uid, fattAttInBrws.ir_attachment_id.id)
        return ''

    def set_name(self, cr, uid, ids, datas_fname, context=None):
        return {'value': {'name': datas_fname}}

    def extract_attachments(self, cr, uid, AttachmentsData, invoice_id):
        AttachModel = self.pool['fatturapa.attachments']
        for attach in AttachmentsData:
            if not attach.NomeAttachment:
                name = _("Attachment without name")
            else:
                name = attach.NomeAttachment
            content = attach.Attachment
            _attach_dict = {
                'name': name,
                'datas': base64.b64encode(str(content)),
                'datas_fname': name,
                'description': attach.DescrizioneAttachment or '',
                'compression': attach.AlgoritmoCompressione or '',
                'format': attach.FormatoAttachment or '',
                'invoice_id': invoice_id,
            }
            AttachModel.create(cr, uid, _attach_dict)
