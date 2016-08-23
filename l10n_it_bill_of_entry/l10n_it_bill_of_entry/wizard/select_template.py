# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2013
#    Associazione OpenERP Italia (<http://www.openerp-italia.org>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _


class wizard_select_invoice_template(orm.TransientModel):
    _inherit = "wizard.select.invoice.template"

    def load_template(self, cr, uid, ids, context=None):
        res = super(wizard_select_invoice_template, self).load_template(cr, uid, ids, context=context)
        if context.get('active_model') == 'account.invoice':
            invoice = self.pool.get('account.invoice').browse(cr, uid,
                context.get('active_id'), context=context)
            if invoice and invoice.customs_doc_type == 'forwarder_invoice':
                invoice_id = res['res_id']
                invoice_obj = self.pool.get('account.invoice')
                invoice_obj.write(cr, uid, invoice_id, {
                    'customs_doc_type': 'bill_of_entry',
                    'forwarder_invoice_id': context.get('active_id')
                }, context=context)
        return res
