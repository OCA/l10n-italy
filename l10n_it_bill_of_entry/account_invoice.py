# -*- coding: utf-8 -*-
#
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
#

from openerp.osv import fields, orm
from openerp.tools.translate import _


class account_invoice(orm.Model):
    _inherit = "account.invoice"

    _columns = {
        'customs_doc_type': fields.selection([
            ('bill_of_entry', 'Bill of Entry'),
            ('supplier_invoice', 'Supplier Invoice'),
            ('forwarder_invoice', 'Forwarder Invoice'),
        ], 'Customs Doc Type', readonly=True),
        'supplier_bill_of_entry_ids': fields.many2many(
            'account.invoice', 'sboe_invoice_rel', 'sboe_id', 'invoice_id',
            'Supplier Bill of Entries', readonly=True),
        'supplier_invoice_ids': fields.many2many(
            'account.invoice', 'sboe_invoice_rel', 'invoice_id', 'sboe_id',
            'Supplier Invoices'),
        'forwarder_invoice_id': fields.many2one(
            'account.invoice', 'Forwarder Invoice'),
        'forwarder_bill_of_entry_ids': fields.one2many(
            'account.invoice', 'forwarder_invoice_id',
            'Forward Bill of Entries', readonly=True),
        'bill_of_entry_storno_id': fields.many2one(
            'account.move', 'Bill of Entry Storno', readonly=True),
    }

    def action_move_create(self, cr, uid, ids, context=None):
        res = super(account_invoice, self).action_move_create(
            cr, uid, ids, context=context)
        move_obj = self.pool.get('account.move')
        move_line_obj = self.pool.get('account.move.line')
        period_obj = self.pool.get('account.period')
        for invoice in self.browse(cr, uid, ids, context):
            if invoice.customs_doc_type == 'forwarder_invoice':
                for bill_of_entry in invoice.forwarder_bill_of_entry_ids:
                    if bill_of_entry.state not in ('open', 'paid'):
                        raise orm.except_orm(
                            _('Error'),
                            _('Bill of entry %s is in state %s')
                            % (
                                bill_of_entry.partner_id.name,
                                bill_of_entry.state))
                advance_customs_vat_line = False
                if invoice.forwarder_bill_of_entry_ids:
                    for line in invoice.invoice_line:
                        if line.advance_customs_vat:
                            advance_customs_vat_line = True
                            break
                if not advance_customs_vat_line:
                    raise orm.except_orm(
                        _('Error'),
                        _("Forwarder invoice %s does not have lines with "
                          "'Adavance Customs Vat'")
                        % invoice.number)
                if not invoice.company_id.bill_of_entry_journal_id:
                    raise orm.except_orm(
                        _('Error'),
                        _('No Bill of entry Storno journal configured'))
                period_ids = period_obj.find(
                    cr, uid, dt=invoice.date_invoice, context=context)
                move_vals = {
                    'period_id': period_ids and period_ids[0] or False,
                    'journal_id': (
                        invoice.company_id.bill_of_entry_journal_id.id),
                    'date': invoice.date_invoice,
                }
                move_lines = []
                for inv_line in invoice.invoice_line:
                    if inv_line.advance_customs_vat:
                        move_lines.append((0, 0, {
                            'name': _("Customs expenses"),
                            'account_id': inv_line.account_id.id,
                            'debit': 0.0,
                            'credit': inv_line.price_subtotal,
                        }))
                for bill_of_entry in invoice.forwarder_bill_of_entry_ids:
                    move_lines.append((0, 0, {
                        'name': _("Customs supplier"),
                        'account_id': bill_of_entry.account_id.id,
                        'debit': bill_of_entry.amount_total,
                        'credit': 0.0,
                        'partner_id': bill_of_entry.partner_id.id,
                    }))
                    for boe_line in bill_of_entry.invoice_line:
                        tax_code_id = False
                        if boe_line.invoice_line_tax_id:
                            if len(boe_line.invoice_line_tax_id) > 1:
                                raise orm.except_orm(
                                    _('Error'),
                                    _("Can't handle more than 1 tax for line "
                                      "%s") % boe_line.name)
                            tax_code_id = (
                                boe_line.invoice_line_tax_id[0].
                                base_code_id and
                                boe_line.invoice_line_tax_id[0].
                                base_code_id.id or False)
                        line_vals = {
                            'name': _("Extra CEE expenses"),
                            'account_id': boe_line.account_id.id,
                            'debit': 0.0,
                            'credit': boe_line.price_subtotal,
                        }
                        if tax_code_id:
                            line_vals['tax_code_id'] = tax_code_id
                            line_vals['tax_amount'] = boe_line.price_subtotal
                        move_lines.append((0, 0, line_vals))
                move_vals['line_id'] = move_lines
                move_id = move_obj.create(cr, uid, move_vals, context=context)
                invoice.write(
                    {'bill_of_entry_storno_id': move_id}, context=context)

                reconcile_ids = []
                for move_line in move_obj.browse(
                    cr, uid, move_id, context
                ).line_id:
                    for bill_of_entry in invoice.forwarder_bill_of_entry_ids:
                        if (
                            move_line.account_id.id ==
                            bill_of_entry.account_id.id
                        ):
                            reconcile_ids.append(move_line.id)
                            for boe_move_line in bill_of_entry.move_id.line_id:
                                if (
                                    boe_move_line.account_id.id ==
                                    bill_of_entry.account_id.id
                                ):
                                    reconcile_ids.append(boe_move_line.id)
                move_line_obj.reconcile_partial(
                    cr, uid, reconcile_ids, type='auto',
                    context=context)
        return res

    def action_cancel(self, cr, uid, ids, context=None):
        account_move_obj = self.pool.get('account.move')
        res = super(account_invoice, self).action_cancel(
            cr, uid, ids, context=context)
        for invoice in self.browse(cr, uid, ids, context):
            if invoice.bill_of_entry_storno_id:
                account_move_obj.button_cancel(
                    cr, uid, [invoice.bill_of_entry_storno_id.id],
                    context=context)
                account_move_obj.unlink(
                    cr, uid, [invoice.bill_of_entry_storno_id.id],
                    context=context)
        return res


class account_invoice_line(orm.Model):
    _inherit = "account.invoice.line"

    _columns = {
        'advance_customs_vat': fields.boolean("Advance Customs Vat"),
    }
