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

from openerp.osv import fields, orm
from openerp.tools.translate import _


class account_invoice(orm.Model):
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

    def action_move_create(self, cr, uid, ids, context=None):
        res = super(account_invoice,self).action_move_create(cr, uid, ids, context=context)
        move_obj = self.pool.get('account.move')
        move_line_obj = self.pool.get('account.move.line')
        period_obj = self.pool.get('account.period')
        for invoice in self.browse(cr, uid, ids, context):
            if invoice.customs_doc_type == 'forwarder_invoice':
                for bill_of_entry in invoice.forwarder_bill_of_entry_ids:
                    if bill_of_entry.state not in ('open', 'paid'):
                        raise orm.except_orm(_('Error'), _('Bill of entry %s is in state %s')
                            % (bill_of_entry.number, bill_of_entry.state))
                advance_customs_vat_line = False
                if invoice.forwarder_bill_of_entry_ids:
                    for line in invoice.invoice_line:
                        if line.advance_customs_vat:
                            advance_customs_vat_line = True
                            break
                if not advance_customs_vat_line:
                    raise orm.except_orm(_('Error'),
                        _("Forwarder invoice %s does not have lines with 'Adavance Customs Vat'")
                        % invoice.number)
                period_ids = period_obj.find(cr, uid, dt=invoice.date, context=context)
                move_vals = {
                    'period_id': period_ids and period_ids[0] or False,
                    }
        return res

class account_invoice_line(orm.Model):
    _inherit = "account.invoice.line"

    _columns = {
        'advance_customs_vat': fields.boolean("Adavance Customs Vat"),
    }
