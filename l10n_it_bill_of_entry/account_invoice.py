# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2013 OpenERP Italia (<http://www.openerp-italia.org>)
#    All Rights Reserved
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

from openerp.osv import fields, osv
from openerp.tools.translate import _


class account_invoice(osv.osv):
    _inherit = "account.invoice"

    _columns = {
        'customs_doc_type': fields.selection([
            ('bill_of_entry', 'Bill of Entry'),
            ('supplier_invoice', 'Supplier Invoice'),
            ('forwarder_invoice', 'Forwarder Invoice'),
        ], 'Customs Doc Type', readonly=True, states={'draft': [('readonly', False)]}),
        'supplier_bill_of_entry_ids': fields.many2many('account.invoice', 'sboe_invoice_rel', 'sboe_id', 'invoice_id', 'Supplier Bill of Entries'),
        'supplier_invoice_ids': fields.many2many('account.invoice', 'invoice_sbe_rel', 'invoice_id', 'sboe_id', 'Supplier Invoices', readonly=True),
        'forwarder_invoice_id': fields.many2one('account.invoice', 'Forwarder Invoice', readonly=True),
        'forwarder_bill_of_entry_ids': fields.one2many('account.invoice', 'forwarder_invoice_id', 'Forward Bill of Entries', readonly=True),
        'bill_of_entry_cancellation_id': fields.many2one('account.move', 'Bill od Entry Cancellation', readonly=True),
    }


class account_invoice_line(osv.osv):
    _inherit = "account.invoice.line"

    _columns = {
        'advance_customs_vat': fields.boolean("Adavance Customs Vat"),
    }
