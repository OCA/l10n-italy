# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Davide Corio <davide.corio@lsweb.it>
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
import logging


class FatturaPAAttachment(orm.Model):
    _name = "fatturapa.attachment.out"
    _description = "E-invoice Export File"
    _inherits = {'ir.attachment': 'ir_attachment_id'}
    _inherit = ['mail.thread']

    def _compute_has_pdf_invoice_print(self, cr, uid, ids, name, unknow_none, context={}):
        ret = {}
        for attachment_out in self.browse(cr, uid, ids, context):
            for invoice in attachment_out.out_invoice_ids:
                invoice_attachments = invoice.fatturapa_doc_attachments
                if any([ia.is_pdf_invoice_print
                        for ia in invoice_attachments]):
                    continue
                else:
                    ret[attachment_out.id] = False
                    break
            else:
                ret[attachment_out.id] = True
        return ret

    def _compute_invoice_partner_id(self, cr, uid, ids, name, unknow_none, context={}):
        ret = {}
        for att in self.browse(cr, uid, ids):
            partners = []
            for invBrws in att.out_invoice_ids:
                invPartner = invBrws.partner_id.id
                if invPartner not in partners:
                    partners.append(invPartner)
            if len(partners) == 1:
                ret[att.id] = partners[0]
        return ret

    def _check_datas_fname(self, cr, uid, ids, context=None):
        for att in self.browse(cr, uid, ids, context):
            res = self.search(cr, uid, [('datas_fname', '=', att.datas_fname)])
            if len(res) > 1:
                return False
        return True

    _columns = {
        'ir_attachment_id': fields.many2one(
            'ir.attachment', 'Attachment', required=True, ondelete="cascade"),
        'out_invoice_ids': fields.one2many(
            'account.invoice', 'fatturapa_attachment_out_id',
            string="Out Invoices", readonly=True),
        'has_pdf_invoice_print': fields.function(_compute_has_pdf_invoice_print, 
                                                 type='boolean', 
                                                 string='Has PDF Invoice Print',
                                                 help="True if all the invoices have a printed "
                                                 "report attached in the XML, False otherwise.",
                                                 store=True),
        'invoice_partner_id': fields.function(_compute_invoice_partner_id, 
                                                 type='many2one', 
                                                 string='Customer',
                                                 store=True,
                                                 relation='res.partner'),
    }
    
    def write(self, cr, uid, ids, vals, context={}):
        res = super(FatturaPAAttachment, self).write(cr, uid, ids, vals, context=context)
        userRead = self.pool.get('res.users').read(cr, uid, uid, ['display_name'], context=context)
        user_name = userRead.get('display_name', str(uid)).replace(',', '')
        logging.info(user_name)
        if 'datas' in vals and 'message_ids' not in vals:
            for attachment in self.browse(cr, uid, ids):
                attachment.message_post(
                    subject=_("E-invoice attachment changed"),
                    body=_("User %s uploaded a new e-invoice file"
                        ) % user_name
                )
        return res

    _constraints = [
        (_check_datas_fname, 'File Already Present.', ['datas_fname']),
    ]


class FatturaAttachments(orm.Model):
    _inherit = "fatturapa.attachments"

    _columns = {
        'is_pdf_invoice_print': fields.boolean(
        help="This attachment contains the PDF report of the linked invoice")
    }
