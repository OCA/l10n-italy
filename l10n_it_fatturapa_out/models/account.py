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
from openerp.tools.translate import _
from openerp.osv import fields, orm
from openerp.osv.osv import except_osv


class account_invoice(orm.Model):
    _inherit = "account.invoice"

    _columns = {
        'fatturapa_attachment_out_id': fields.many2one(
            'fatturapa.attachment.out', 'E-invoice Export File',
            readonly=True),
        'has_pdf_invoice_print': fields.related('fatturapa_attachment_out_id', 'has_pdf_invoice_print',
                                                type='boolean', relation='fatturapa.attachment.out',
                                                string='Has PDF invoice', readonly=True),
    }

    def preventive_checks(self, cr, uid, ids, context={}):
        # hook for preventive checks. Override and raise exception, in case
        return

    def action_invoice_cancel(self, cr, uid, ids, context={}):
        for invoice in self.browse(cr, uid, ids, context):
            if invoice.fatturapa_attachment_out_id:
                raise except_osv(_('Error' ),
                                 _(
                    "Invoice %s has XML and can't be canceled. "
                    "Delete the XML before"
                ) % invoice.number)
        res = super(account_invoice, self).action_invoice_cancel(cr, uid, ids, context)
        return res