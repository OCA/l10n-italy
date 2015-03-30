# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Abstract (http://www.abstract.it)
#    Author: Davide Corio <davide.corio@abstract.it>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api


class AccountRCType(models.Model):
    _name = 'account.rc.type'
    _description = 'Reverse Charge Type'

    name = fields.Char('Name')
    method = fields.Selection(
        (('integration', 'VAT Integration'),
            ('selfinvoice', 'Self Invoice')),
        string='Method')
    partner_type = fields.Selection(
        (('supplier', 'Supplier'), ('other', 'Other')),
        string='Self Invoice Partner Type')
    partner_id = fields.Many2one(
        'res.partner',
        string='Self Invoice Partner',
        help="Partner used on RC self invoices.")
    journal_id = fields.Many2one(
        'account.journal',
        string='Self Invoice Journal',
        help="Journal used on RC self invoices.")
    payment_journal_id = fields.Many2one(
        'account.journal',
        string='Self Invoice Payment Journal',
        help="Journal used to pay RC self invoices.")
    payment_partner_id = fields.Many2one(
        'res.partner',
        string='Self Invoice Payment Partner',
        help="Partner used on RC self invoices.")
    transitory_account_id = fields.Many2one(
        'account.account',
        string='Self Invoice Transitory Account',
        help="Transitory account used on self invoices.")
    tax_id = fields.Many2one('account.tax', string='Self Invoice Line Tax')
    description = fields.Text('Description')
    invoice_text = fields.Text('Text on Invoice')
    self_invoice_text = fields.Text('Text in Self Invoice')


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    rc_type_id = fields.Many2one('account.rc.type', 'RC Type')


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    rc = fields.Boolean("RC")


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    rc_self_invoice_id = fields.Many2one('account.invoice', 'RC Self Invoice')
    rc_purchase_invoice_id = fields.Many2one(
        'account.invoice', 'RC Purchase Invoice')

    @api.multi
    def action_move_create(self):
        super(AccountInvoice, self).action_move_create()
        if self.fiscal_position.rc_type_id and \
                self.fiscal_position.rc_type_id.method == 'integration':
            for line in self.move_id.line_id:
                if not line.debit and not line.credit:
                    line.skip = True

    def rc_inv_line_vals(self, line):
        return {
            'product_id': line.product_id.id,
            'name': line.name,
            'uom_id': line.uos_id.id,
            'price_unit': line.price_unit,
            'quantity': line.quantity,
            }

    def rc_inv_vals(self, partner, account, rc_type, lines):
        return {
            'partner_id': partner.id,
            'type': 'out_invoice',
            'account_id': account.id,
            'journal_id': rc_type.journal_id.id,
            'invoice_line': lines,
            'date_invoice': self.registration_date,
            'registration_date': self.registration_date,
            'origin': self.number,
            'rc_purchase_invoice_id': self.id,
            }

    def get_inv_line_to_reconcile(self):
        for inv_line in self.move_id.line_id:
            if inv_line.credit:
                return inv_line
        return False

    def get_rc_inv_line_to_reconcile(self, invoice):
        for inv_line in invoice.move_id.line_id:
            if inv_line.debit:
                return inv_line
        return False

    def rc_payment_vals(self, rc_type):
        return {
            'journal_id': rc_type.payment_journal_id.id,
            'period_id': self.period_id.id,
            'date': self.registration_date,
            }

    def rc_credit_line_vals(self, journal, move):
        return {
            'name': self.number,
            'credit': self.amount_tax,
            'debit': 0.0,
            'account_id': journal.default_credit_account_id.id,
            'move_id': move.id,
            }

    def rc_debit_line_vals(self, journal, move, rc_type):
        return {
            'name': self.number,
            'debit': self.amount_tax,
            'credit': 0.0,
            'account_id': self.get_inv_line_to_reconcile().account_id.id,
            'move_id': move.id,
            'partner_id': self.partner_id.id,
            }

    def rc_invoice_payment_vals(self, rc_type):
        return {
            'journal_id': rc_type.payment_journal_id.id,
            'period_id': self.period_id.id,
            'date': self.registration_date,
            }

    def rc_payment_credit_line_vals(self, invoice, move):
        return {
            'name': invoice.number,
            'credit': self.get_rc_inv_line_to_reconcile(invoice).debit,
            'debit': 0.0,
            'account_id': self.get_rc_inv_line_to_reconcile(
                invoice).account_id.id,
            'move_id': move.id,
            'partner_id': invoice.partner_id.id,
            }

    def rc_payment_debit_line_vals(self, invoice, journal, move):
        return {
            'name': invoice.number,
            'debit': self.get_rc_inv_line_to_reconcile(invoice).debit,
            'credit': 0.0,
            'account_id': journal.default_credit_account_id.id,
            'move_id': move.id,
            }

    @api.multi
    def invoice_validate(self):
        res = super(AccountInvoice, self).invoice_validate()

        invoice_model = self.env['account.invoice']
        move_model = self.env['account.move']
        move_line_model = self.env['account.move.line']

        fp = self.fiscal_position
        rc_type = fp and fp.rc_type_id
        if rc_type and rc_type.method == 'selfinvoice':
            if rc_type.partner_type == 'other':
                rc_partner = rc_type.partner_id
            else:
                rc_partner = self.partner_id
            rc_account = rc_partner.property_account_receivable

            rc_invoice_lines = []
            for line in self.invoice_line:
                if line.rc:
                    rc_invoice_line = self.rc_inv_line_vals(line)
                    line_tax = line.invoice_line_tax_id
                    if line_tax:
                        rc_invoice_line['invoice_line_tax_id'] = [
                            (6, False, [rc_type.tax_id.id])]
                    rc_invoice_line[
                        'account_id'] = rc_type.transitory_account_id.id
                    rc_invoice_lines.append([0, False, rc_invoice_line])

            if rc_invoice_lines:
                invoice_data = self.rc_inv_vals(
                    rc_partner, rc_account, rc_type, rc_invoice_lines)
                rc_invoice = invoice_model.create(invoice_data)
                self.rc_self_invoice_id = rc_invoice.id
                rc_invoice.signal_workflow('invoice_open')

                ## partially reconcile purchase invoice
                rc_payment_data = self.rc_payment_vals(rc_type)
                rc_payment = move_model.create(rc_payment_data)

                payment_credit_line_data = self.rc_credit_line_vals(
                    rc_type.payment_journal_id, rc_payment)
                move_line_model.create(payment_credit_line_data)

                payment_debit_line_data = self.rc_debit_line_vals(
                    rc_type.payment_journal_id, rc_payment, rc_type)
                payment_debit_line = move_line_model.create(
                    payment_debit_line_data)
                inv_lines_to_rec = move_line_model.browse(
                    [self.get_inv_line_to_reconcile().id,
                        payment_debit_line.id])
                inv_lines_to_rec.reconcile_partial()

                ## reconcile rc invoice
                rc_payment_credit_line_data = self.rc_payment_credit_line_vals(
                    rc_invoice, rc_payment)

                rc_payment_line_to_reconcile = move_line_model.create(
                    rc_payment_credit_line_data)

                rc_payment_debit_line_data = self.rc_payment_debit_line_vals(
                    rc_invoice, rc_type.payment_journal_id, rc_payment)
                move_line_model.create(
                    rc_payment_debit_line_data)

                rc_lines_to_rec = move_line_model.browse(
                    [self.get_rc_inv_line_to_reconcile(rc_invoice).id,
                        rc_payment_line_to_reconcile.id])
                rc_lines_to_rec.reconcile_partial()

        return res
