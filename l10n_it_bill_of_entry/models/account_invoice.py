# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013-2017 Agile Business Group sagl (http://www.agilebg.com)
#    @author Alex Comba <alex.comba@agilebg.com>
#    @author Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#    Copyright (C) 2017 CQ Creativi Quadrati (http://www.creativiquadrati.it)
#    @author Diego Bruselli <d.bruselli@creativiquadrati.it>
#    Copyright (C) 2013
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
##############################################################################

from odoo import fields, models, api
from odoo.tools.translate import _
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    customs_doc_type = fields.Selection([
        ('bill_of_entry', 'Bill of Entry'),
        ('supplier_invoice', 'Supplier Invoice'),
        ('forwarder_invoice', 'Forwarder Invoice'),
    ], 'Customs Doc Type', readonly=True)
    supplier_bill_of_entry_ids = fields.Many2many(
        'account.invoice', 'sboe_invoice_rel', 'sboe_id', 'invoice_id',
        'Supplier Bill of Entries', readonly=True)
    supplier_invoice_ids = fields.Many2many(
        'account.invoice', 'sboe_invoice_rel', 'invoice_id', 'sboe_id',
        'Supplier Invoices')
    forwarder_invoice_id = fields.Many2one(
        'account.invoice', 'Forwarder Invoice')
    forwarder_bill_of_entry_ids = fields.One2many(
        'account.invoice', 'forwarder_invoice_id',
        'Forward Bill of Entries', readonly=True)
    bill_of_entry_storno_id = fields.Many2one(
        'account.move', 'Bill of Entry Storno', readonly=True)

    @api.multi
    def action_move_create(self):
        res = super(AccountInvoice, self).action_move_create()

        AccountMove = self.env['account.move']
        AccountMoveLine = self.env['account.move.line']
        for invoice in self:
            if invoice.customs_doc_type == 'forwarder_invoice':
                for bill_of_entry in invoice.forwarder_bill_of_entry_ids:
                    if bill_of_entry.state not in ('open', 'paid'):
                        raise UserError(
                            _('Bill of entry %s is in state %s')
                            % (
                                bill_of_entry.partner_id.name,
                                bill_of_entry.state)
                        )
                advance_customs_vat_line = False
                if invoice.forwarder_bill_of_entry_ids:
                    for line in invoice.invoice_line_ids:
                        if line.advance_customs_vat:
                            advance_customs_vat_line = True
                            break
                if not advance_customs_vat_line:
                    raise UserError(
                        _("Forwarder invoice %s does not have lines with "
                          "'Advance Customs Vat'")
                        % invoice.number)
                if not invoice.company_id.bill_of_entry_journal_id:
                    raise UserError(
                        _('No Bill of entry Storno journal configured')
                    )
                move_vals = {
                    'journal_id': (
                        invoice.company_id.bill_of_entry_journal_id.id),
                    'date': invoice.date_invoice,
                }
                move_lines = []
                for inv_line in invoice.invoice_line_ids:
                    if inv_line.advance_customs_vat:
                        line_vals = {
                            'name': _("Customs expenses"),
                            'account_id': inv_line.account_id.id,
                            'debit': 0.0,
                            'credit': inv_line.price_subtotal,
                            'partner_id': inv_line.partner_id.id,
                        }
                        if inv_line.product_id:
                            line_vals['product_id'] = inv_line.product_id.id
                        move_lines.append((0, 0, line_vals))
                for bill_of_entry in invoice.forwarder_bill_of_entry_ids:
                    line_vals = {
                        'name': _("Customs supplier"),
                        'account_id': bill_of_entry.account_id.id,
                        'debit': bill_of_entry.amount_total,
                        'credit': 0.0,
                        'partner_id': bill_of_entry.partner_id.id,
                    }
                    move_lines.append((0, 0, line_vals))
                    for boe_line in bill_of_entry.invoice_line_ids:
                        if boe_line.invoice_line_tax_ids:
                            if len(boe_line.invoice_line_tax_ids) > 1:
                                raise UserError(
                                    _("Can't handle more than 1 tax for line "
                                      "%s") % boe_line.name)

                        line_vals = {
                            'name': _("Extra CEE expenses"),
                            'account_id': boe_line.account_id.id,
                            'debit': 0.0,
                            'credit': boe_line.price_subtotal,
                            'partner_id': boe_line.partner_id.id,
                        }
                        if boe_line.product_id:
                            line_vals['product_id'] = boe_line.product_id.id
                        move_lines.append((0, 0, line_vals))
                move_vals['line_ids'] = move_lines
                move = AccountMove.create(move_vals)
                invoice.write(
                    {'bill_of_entry_storno_id': move.id})

                reconcile_ids = []
                for move_line in move.line_ids:
                    for boe in invoice.forwarder_bill_of_entry_ids:
                        if (
                            move_line.account_id.id ==
                            boe.account_id.id
                        ):
                            reconcile_ids.append(move_line.id)
                            for boe_move_line in boe.move_id.line_ids:
                                if (
                                    boe_move_line.account_id.id ==
                                    boe.account_id.id
                                ):
                                    reconcile_ids.append(boe_move_line.id)

                AccountMoveLine.browse(reconcile_ids).reconcile()
        return res

    def action_cancel(self):
        res = super(AccountInvoice, self).action_cancel()
        for invoice in self:
            if invoice.bill_of_entry_storno_id:
                invoice.bill_of_entry_storno_id.button_cancel()
                invoice.bill_of_entry_storno_id.unlink()
        return res


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    advance_customs_vat = fields.Boolean("Advance Customs Vat")
