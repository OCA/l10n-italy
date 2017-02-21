# -*- coding: utf-8 -*-
# Copyright 2017 Davide Corio
# Copyright 2017 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.onchange('invoice_line_tax_id')
    def onchange_invoice_line_tax_id(self):
        fposition = self.invoice_id.fiscal_position
        self.rc = True if fposition.rc_type_id else False

    rc = fields.Boolean("RC")


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    rc_self_invoice_id = fields.Many2one(
        comodel_name='account.invoice',
        string='RC Self Invoice',
        copy=False)
    rc_purchase_invoice_id = fields.Many2one(
        comodel_name='account.invoice',
        string='RC Purchase Invoice')

    def rc_inv_line_vals(self, line):
        return {
            'name': line.name,
            'uos_id': line.uos_id.id,
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
            'name': rc_type.self_invoice_text,
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
        self.ensure_one()
        res = super(AccountInvoice, self).invoice_validate()

        invoice_model = self.env['account.invoice']
        move_model = self.env['account.move']
        move_line_model = self.env['account.move.line']

        fp = self.fiscal_position
        rc_type = fp and fp.rc_type_id
        if rc_type and rc_type.method == 'selfinvoice':
            if not rc_type.payment_journal_id.default_credit_account_id:
                raise UserError(
                    _('There is no default credit account defined \n'
                      'on journal "%s".') % rc_type.payment_journal_id.name)
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
                    for tax_mapping in rc_type.tax_ids:
                        if tax_mapping.purchase_tax_id == line_tax[0]:
                            tax_code_id = tax_mapping.sale_tax_id.id
                    if line_tax:
                        rc_invoice_line['invoice_line_tax_id'] = [
                            (6, False, [tax_code_id])]
                    rc_invoice_line[
                        'account_id'] = rc_type.transitory_account_id.id
                    rc_invoice_lines.append([0, False, rc_invoice_line])

            if rc_invoice_lines:
                inv_vals = self.rc_inv_vals(
                    rc_partner, rc_account, rc_type, rc_invoice_lines)

                # create or write the self invoice
                if self.rc_self_invoice_id:
                    rc_invoice = self.rc_self_invoice_id
                    rc_invoice.invoice_line.unlink()
                    rc_invoice.period_id = False
                    rc_invoice.write(inv_vals)
                    rc_invoice.button_reset_taxes()
                else:
                    rc_invoice = invoice_model.create(inv_vals)
                    self.rc_self_invoice_id = rc_invoice.id
                rc_invoice.signal_workflow('invoice_open')

                # partially reconcile supplier invoice
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

                # reconcile rc invoice
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

    @api.multi
    def action_cancel(self):
        invoice_model = self.env['account.invoice']
        for inv in self:
            rc_type = inv.fiscal_position.rc_type_id
            if (
                    rc_type and
                    rc_type.method == 'selfinvoice' and
                    inv.rc_self_invoice_id
            ):
                if len(inv.payment_ids) > 1:
                    raise UserError(
                        _('There are more than one payment line.\n'
                          'In that case account entries cannot be canceled'
                          'automatically. Please proceed manually'))
                payment_move = inv.payment_ids[0].move_id
                # remove move reconcile related to the supplier invoice
                move = inv.move_id
                rec_partial_lines = move.mapped('line_id').filtered(
                    'reconcile_partial_id').mapped(
                    'reconcile_partial_id.line_partial_ids')
                self.env['account.move.line']._remove_move_reconcile(
                    rec_partial_lines.ids)
                # remove move reconcile related to the self invoice
                move = inv.rc_self_invoice_id.move_id
                rec_lines = move.mapped('line_id').filtered(
                    'reconcile_id').mapped('reconcile_id.line_id')
                self.env['account.move.line']._remove_move_reconcile(
                    rec_lines.ids)
                # cancel self invoice
                self_invoice = invoice_model.browse(
                    inv.rc_self_invoice_id.id)
                self_invoice.signal_workflow('invoice_cancel')
                # invalidate and delete the payment move generated
                # by the self invoice creation
                payment_move.button_cancel()
                payment_move.unlink()
        return super(AccountInvoice, self).action_cancel()

    @api.multi
    def action_cancel_draft(self):
        super(AccountInvoice, self).action_cancel_draft()
        invoice_model = self.env['account.invoice']
        for inv in self:
            if inv.rc_self_invoice_id:
                self_invoice = invoice_model.browse(
                    inv.rc_self_invoice_id.id)
                self_invoice.action_cancel_draft()
        return True
