# -*- coding: utf-8 -*-
# Copyright 2017 Davide Corio
# Copyright 2017 Alex Comba - Agile Business Group
# Copyright 2017 Lorenzo Battistini - Agile Business Group
# Copyright 2017 Marco Calcagni - Dinamiche Aziendali srl
# Copyright 2022 Simone Rubino - TAKOBI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    rc = fields.Boolean("RC")

    @api.multi
    def _set_rc_flag(self, invoice):
        self.ensure_one()
        if invoice.type in ['in_invoice', 'in_refund']:
            fposition = invoice.fiscal_position
            self.rc = bool(fposition.rc_type_id)

    @api.onchange('invoice_line_tax_id')
    def onchange_invoice_line_tax_id(self):
        self._set_rc_flag(self.invoice_id)

    @api.model
    def create(self, vals):
        if 'rc' not in vals and 'invoice_id' in vals:
            invoice = self.env['account.invoice'].browse(vals['invoice_id'])
            fiscal_position = invoice.fiscal_position
            vals.update({'rc': True if fiscal_position.rc_type_id else False})

        return super(AccountInvoiceLine, self).create(vals)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    rc_self_invoice_id = fields.Many2one(
        comodel_name='account.invoice',
        string='RC Self Invoice',
        copy=False, readonly=True)
    rc_purchase_invoice_id = fields.Many2one(
        comodel_name='account.invoice',
        string='RC Purchase Invoice', copy=False, readonly=True)
    rc_self_purchase_invoice_id = fields.Many2one(
        comodel_name='account.invoice',
        string='RC Self Purchase Invoice', copy=False, readonly=True)

    @api.onchange('fiscal_position')
    def onchange_rc_fiscal_position_id(self):
        for line in self.invoice_line:
            line._set_rc_flag(self)

    @api.multi
    @api.onchange('partner_id', 'company_id')
    def onchange_partner_id(self, invoice_type, partner_id, date_invoice=False,
                            payment_term=False, partner_bank_id=False,
                            company_id=False):
        res = super(AccountInvoice, self).onchange_partner_id(
            invoice_type, partner_id, date_invoice=date_invoice,
            payment_term=payment_term, partner_bank_id=partner_bank_id,
            company_id=company_id)
        # In some cases (like creating the invoice from PO),
        # fiscal position's onchange is triggered
        # before than being changed by this method.
        self.onchange_rc_fiscal_position_id()
        return res

    @api.multi
    def _get_original_suppliers(self):
        rc_purchase_invoices = self.mapped("rc_purchase_invoice_id")
        supplier_invoices = self.env["account.invoice"]
        for rc_purchase_invoice in rc_purchase_invoices:
            current_supplier_invoices = self.search([
                ("rc_self_purchase_invoice_id", "=", rc_purchase_invoice.id)
            ])
            if current_supplier_invoices:
                supplier_invoices |= current_supplier_invoices
            else:
                supplier_invoices |= rc_purchase_invoice
        return supplier_invoices.mapped("partner_id")

    def rc_inv_line_vals(self, line):
        return {
            'name': line.name,
            'uos_id': line.uos_id.id,
            'price_unit': line.price_unit,
            'quantity': line.quantity,
            'discount': line.discount,
            }

    def rc_inv_vals(self, partner, account, rc_type, lines):
        if self.type == 'in_invoice':
            type = 'out_invoice'
        else:
            type = 'out_refund'
        supplier = self.partner_id
        original_invoice = self.search([
            ("rc_self_purchase_invoice_id", "=", self.id)
        ], limit=1)
        if original_invoice:
            supplier = original_invoice.partner_id

        comment = _(
            "Reverse charge self invoice.\n"
            "Supplier: %s\n"
            "Reference: %s\n"
            "Date: %s\n"
            "Internal reference: %s") % (
            supplier.display_name, self.reference or '', self.date_invoice,
            self.number
        )
        return {
            'partner_id': partner.id,
            'type': type,
            'account_id': account.id,
            'journal_id': rc_type.journal_id.id,
            'invoice_line': lines,
            'date_invoice': self.registration_date,
            'registration_date': self.registration_date,
            'origin': self.number,
            'rc_purchase_invoice_id': self.id,
            'name': rc_type.self_invoice_text,
            'comment': comment,
            }

    def get_inv_line_to_reconcile(self):
        for inv_line in self.move_id.line_id:
            if (self.type == 'in_invoice') and inv_line.credit:
                return inv_line
            elif (self.type == 'in_refund') and inv_line.debit:
                return inv_line
        return False

    def get_rc_inv_line_to_reconcile(self, invoice):
        for inv_line in invoice.move_id.line_id:
            if (invoice.type == 'out_invoice') and inv_line.debit:
                return inv_line
            elif (invoice.type == 'out_refund') and inv_line.credit:
                return inv_line
        return False

    def rc_payment_vals(self, rc_type):
        return {
            'journal_id': rc_type.payment_journal_id.id,
            'period_id': self.period_id.id,
            'date': self.registration_date,
            }

    def compute_rc_amount_tax(self):
        rc_amount_tax = 0.0
        round_curr = self.currency_id.round
        rc_lines = self.invoice_line.filtered(lambda l: l.rc)
        for rc_line in rc_lines:
            price_unit = \
                rc_line.price_unit * (1 - (rc_line.discount or 0.0) / 100.0)
            taxes = rc_line.invoice_line_tax_id.compute_all(
                price_unit,
                rc_line.quantity,
                product=rc_line.product_id,
                partner=rc_line.partner_id)['taxes']
            rc_amount_tax += sum([tax['amount'] for tax in taxes])

        # convert the amount to main company currency, as
        # compute_rc_amount_tax is used for debit/credit fields
        invoice_currency = self.currency_id.with_context(
            date=self.date_invoice)
        main_currency = self.company_id.currency_id.with_context(
            date=self.date_invoice)
        if invoice_currency != main_currency:
            round_curr = main_currency.round
            rc_amount_tax = invoice_currency.compute(
                rc_amount_tax, main_currency)

        return round_curr(rc_amount_tax)

    def rc_credit_line_vals(self, journal, move):
        credit = debit = 0.0
        amount_rc_tax = self.compute_rc_amount_tax()

        if self.type == 'in_invoice':
            credit = amount_rc_tax
        else:
            debit = amount_rc_tax

        return {
            'name': self.number,
            'credit': credit,
            'debit': debit,
            'account_id': journal.default_credit_account_id.id,
            'move_id': move.id,
            }

    def rc_debit_line_vals(self, move, amount=None):
        credit = debit = 0.0

        if self.type == 'in_invoice':
            if amount:
                debit = amount
            else:
                debit = self.compute_rc_amount_tax()
        else:
            if amount:
                credit = amount
            else:
                credit = self.compute_rc_amount_tax()
        return {
            'name': self.number,
            'debit': debit,
            'credit': credit,
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
        credit = debit = 0.0
        if invoice.type == 'out_invoice':
            credit = self.get_rc_inv_line_to_reconcile(invoice).debit
        else:
            debit = self.get_rc_inv_line_to_reconcile(invoice).credit
        return {
            'name': invoice.number,
            'credit': credit,
            'debit': debit,
            'account_id': self.get_rc_inv_line_to_reconcile(
                invoice).account_id.id,
            'move_id': move.id,
            'partner_id': invoice.partner_id.id,
            }

    def rc_payment_debit_line_vals(self, invoice, journal, move):
        credit = debit = 0.0
        if invoice.type == 'out_invoice':
            debit = self.get_rc_inv_line_to_reconcile(invoice).debit
        else:
            credit = self.get_rc_inv_line_to_reconcile(invoice).credit
        return {
            'name': invoice.number,
            'debit': debit,
            'credit': credit,
            'account_id': journal.default_credit_account_id.id,
            'move_id': move.id,
            }

    def reconcile_supplier_invoice(self):
        rc_type = self.fiscal_position.rc_type_id
        move_model = self.env['account.move']
        move_line_model = self.env['account.move.line']
        rc_payment_data = self.rc_payment_vals(rc_type)
        rc_payment = move_model.create(rc_payment_data)
        rc_invoice = self.rc_self_invoice_id

        payment_credit_line_data = self.rc_payment_credit_line_vals(
            rc_invoice, rc_payment)
        payment_credit_line = move_line_model.create(payment_credit_line_data)
        payment_debit_line_data = self.rc_debit_line_vals(
            rc_payment, self.amount_total)
        payment_debit_line = move_line_model.create(
            payment_debit_line_data)
        rc_payment.post()

        lines_to_rec = move_line_model.browse([
            self.get_inv_line_to_reconcile().id,
            payment_debit_line.id
        ])
        lines_to_rec.reconcile_partial()

        rc_lines_to_rec = move_line_model.browse([
            self.get_rc_inv_line_to_reconcile(rc_invoice).id,
            payment_credit_line.id
        ])
        rc_lines_to_rec.reconcile_partial()

    def partially_reconcile_supplier_invoice(self):
        rc_type = self.fiscal_position.rc_type_id
        move_model = self.env['account.move']
        move_line_model = self.env['account.move.line']
        rc_payment_data = self.rc_payment_vals(rc_type)
        rc_payment = move_model.create(rc_payment_data)

        payment_credit_line_data = self.rc_credit_line_vals(
            rc_type.payment_journal_id, rc_payment)
        move_line_model.create(payment_credit_line_data)

        payment_debit_line_data = self.rc_debit_line_vals(rc_payment)
        payment_debit_line = move_line_model.create(
            payment_debit_line_data)
        inv_lines_to_rec = move_line_model.browse(
            [self.get_inv_line_to_reconcile().id,
                payment_debit_line.id])
        inv_lines_to_rec.reconcile_partial()
        return rc_payment

    def reconcile_rc_invoice(self, rc_payment):
        rc_type = self.fiscal_position.rc_type_id
        move_line_model = self.env['account.move.line']
        rc_invoice = self.rc_self_invoice_id
        rc_payment_credit_line_data = self.rc_payment_credit_line_vals(
            rc_invoice, rc_payment)

        rc_payment_line_to_reconcile = move_line_model.create(
            rc_payment_credit_line_data)

        rc_payment_debit_line_data = self.rc_payment_debit_line_vals(
            rc_invoice, rc_type.payment_journal_id, rc_payment)
        move_line_model.create(
            rc_payment_debit_line_data)
        rc_payment.post()

        rc_lines_to_rec = move_line_model.browse(
            [self.get_rc_inv_line_to_reconcile(rc_invoice).id,
                rc_payment_line_to_reconcile.id])
        rc_lines_to_rec.reconcile_partial()

    def generate_self_invoice(self):
        rc_type = self.fiscal_position.rc_type_id
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
                line_tax_ids = line.invoice_line_tax_id
                if not line_tax_ids:
                    raise UserError(_(
                        "Invoice %s, line\n%s\nis RC but has not tax"
                    ) % ((self.reference or self.partner_id.display_name), line.name))
                mapped_taxes = rc_type.map_tax(
                    line_tax_ids,
                    'purchase_tax_id',
                    'sale_tax_id',
                )
                if line_tax_ids and mapped_taxes:
                    rc_invoice_line['invoice_line_tax_id'] = [
                        (6, False, mapped_taxes.ids)]
                rc_invoice_line[
                    'account_id'] = rc_type.transitory_account_id.id
                rc_invoice_lines.append([0, False, rc_invoice_line])

        if rc_invoice_lines:
            inv_vals = self.rc_inv_vals(
                rc_partner, rc_account, rc_type, rc_invoice_lines)

            # create or write the self invoice
            if self.rc_self_invoice_id:
                # this is needed when user takes back to draft supplier
                # invoice, edit and validate again
                rc_invoice = self.rc_self_invoice_id
                rc_invoice.invoice_line.unlink()
                rc_invoice.period_id = False
                rc_invoice.write(inv_vals)
                rc_invoice.button_reset_taxes()
            else:
                rc_invoice = self.create(inv_vals)
                self.rc_self_invoice_id = rc_invoice.id
            rc_invoice.signal_workflow('invoice_open')
            if rc_type.with_supplier_self_invoice:
                self.reconcile_supplier_invoice()
            else:
                rc_payment = self.partially_reconcile_supplier_invoice()
                self.reconcile_rc_invoice(rc_payment)

    def generate_supplier_self_invoice(self):
        rc_type = self.fiscal_position.rc_type_id
        if not self.rc_self_purchase_invoice_id:
            supplier_invoice = self.copy()
        else:
            supplier_invoice_vals = self.copy_data()
            supplier_invoice = self.rc_self_purchase_invoice_id
            supplier_invoice.invoice_line.unlink()
            supplier_invoice.write(supplier_invoice_vals[0])

        # because this field has copy=False
        supplier_invoice.registration_date = self.registration_date
        supplier_invoice.date_invoice = self.registration_date
        supplier_invoice.date_due = self.registration_date
        supplier_invoice.partner_id = rc_type.partner_id.id
        supplier_invoice.journal_id = rc_type.supplier_journal_id.id
        for inv_line in supplier_invoice.invoice_line:
            line_tax_ids = inv_line.invoice_line_tax_id
            mapped_taxes = rc_type.map_tax(
                line_tax_ids,
                'original_purchase_tax_id',
                'purchase_tax_id',
            )
            if line_tax_ids and mapped_taxes:
                inv_line.invoice_line_tax_id = [
                    (6, False, mapped_taxes.ids),
                ]

            inv_line.account_id = rc_type.transitory_account_id.id
        self.rc_self_purchase_invoice_id = supplier_invoice.id

        # temporary disabling self invoice automations
        supplier_invoice.fiscal_position = None
        supplier_invoice.button_reset_taxes()
        supplier_invoice.check_total = supplier_invoice.amount_total
        supplier_invoice.signal_workflow('invoice_open')
        supplier_invoice.fiscal_position = self.fiscal_position.id

    @api.multi
    def invoice_validate(self):
        res = super(AccountInvoice, self).invoice_validate()
        for invoice in self:
            fp = invoice.fiscal_position
            rc_type = fp and fp.rc_type_id
            if not rc_type:
                continue
            if rc_type.method == 'selfinvoice':
                if not rc_type.with_supplier_self_invoice:
                    invoice.generate_self_invoice()
                else:
                    # See with_supplier_self_invoice field help
                    invoice.generate_supplier_self_invoice()
                    invoice.rc_self_purchase_invoice_id.generate_self_invoice()
            elif rc_type.method == 'integration':
                raise UserError(
                    _("VAT integration RC type, "
                      "defined in fiscal position %s, is not managed yet")
                    % fp.display_name)
        return res

    def remove_rc_payment(self):
        inv = self
        if inv.payment_ids:
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
            # also remove full reconcile, in case of with_supplier_self_invoice
            rec_partial_lines = move.mapped('line_id').filtered(
                'reconcile_id').mapped('reconcile_id.line_id')
            self.env['account.move.line']._remove_move_reconcile(
                rec_partial_lines.ids)
            # remove move reconcile related to the self invoice
            move = inv.rc_self_invoice_id.move_id
            rec_lines = move.mapped('line_id').filtered(
                'reconcile_id').mapped('reconcile_id.line_id')
            self.env['account.move.line']._remove_move_reconcile(
                rec_lines.ids)
            # cancel self invoice
            self_invoice = self.browse(
                inv.rc_self_invoice_id.id)
            self_invoice.signal_workflow('invoice_cancel')
            # invalidate and delete the payment move generated
            # by the self invoice creation
            payment_move.button_cancel()
            payment_move.unlink()

    @api.multi
    def action_cancel(self):
        for inv in self:
            rc_type = inv.fiscal_position.rc_type_id
            if (
                rc_type and
                rc_type.method == 'selfinvoice' and
                inv.rc_self_invoice_id
            ):
                inv.remove_rc_payment()
            elif (
                rc_type and
                rc_type.method == 'selfinvoice' and
                inv.rc_self_purchase_invoice_id
            ):
                inv.rc_self_purchase_invoice_id.remove_rc_payment()
                inv.rc_self_purchase_invoice_id.signal_workflow(
                    'invoice_cancel')
        return super(AccountInvoice, self).action_cancel()

    @api.multi
    def action_cancel_draft(self):
        new_self = self.with_context(rc_set_to_draft=True)
        super(AccountInvoice, new_self).action_cancel_draft()
        invoice_model = new_self.env['account.invoice']
        for inv in new_self:
            if inv.rc_self_invoice_id:
                self_invoice = invoice_model.browse(
                    inv.rc_self_invoice_id.id)
                self_invoice.action_cancel_draft()
            if inv.rc_self_purchase_invoice_id:
                self_purchase_invoice = invoice_model.browse(
                    inv.rc_self_purchase_invoice_id.id)
                self_purchase_invoice.action_cancel_draft()
        return True

    @api.multi
    def get_tax_amount_added_for_rc(self):
        self.ensure_one()
        res = 0
        for line in self.invoice_line:
            if line.rc:
                price_unit = line.price_unit * (
                    1 - (line.discount or 0.0) / 100.0)
                taxes = line.invoice_line_tax_id.compute_all(
                    price_unit,
                    line.quantity,
                    product=line.product_id,
                    partner=self.partner_id)['taxes']
                for tax in taxes:
                    res += tax['amount']
        return res
