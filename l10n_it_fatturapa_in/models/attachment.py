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

from openerp.osv import fields, orm


class FatturaPAAttachmentIn(orm.Model):
    _name = "fatturapa.attachment.in"
    _description = "FatturaPA import File"
    _inherits = {'ir.attachment': 'ir_attachment_id'}
    _inherit = ['mail.thread']
    _order = 'id desc'

    def _compute_xml_data(self, cr, uid, ids, context={}):
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
            self.write(cr, uid, [att.id], vals)

    def _compute_registered(self, cr, uid, ids, context={}):
        for att in self.browse(cr, uid, ids, context):
            vals = {}
            if (att.in_invoice_ids and len(att.in_invoice_ids) == att.invoices_number):
                vals['registered'] = True
            else:
                vals['registered'] = False
            self.write(cr, uid, [att.id], vals)

    _columns = {
        'ir_attachment_id': fields.many2one(
            'ir.attachment', 'Attachment', required=True, ondelete="cascade"),
        'in_invoice_ids': fields.one2many(
            'account.invoice', 'fatturapa_attachment_in_id',
            string="In Invoices", readonly=True),
        #TODO: Imported fields
        'xml_supplier_id': fields.function(_compute_xml_data, 
                                           method=True, 
                                           string="Supplier", 
                                           type="many2one"),
        'invoices_number': fields.function(_compute_xml_data, 
                                           method=True, 
                                           string="Invoices number", 
                                           type="integer"),
        'invoices_total': fields.function(_compute_xml_data, 
                                           method=True, 
                                           string="Invoices total", 
                                           type="float",
                                           help="Se indicato dal fornitore, Importo totale del documento al "
                 "netto dell'eventuale sconto e comprensivo di imposta a debito "
                 "del cessionario / committente"),
        'registered': fields.function(_compute_registered, 
                                           method=True, 
                                           string="Registered", 
                                           type="boolean"),
    }

    def get_xml_string(self):
        return self.ir_attachment_id.get_xml_string()

    def set_name(self, cr, uid, ids, datas_fname, context=None):
        return {'value': {'name': datas_fname}}

