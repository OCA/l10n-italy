# Copyright 2016 Davide Corio
# Copyright 2017 Alex Comba - Agile Business Group
# Copyright 2017 Lorenzo Battistini - Agile Business Group
# Copyright 2017 Marco Calcagni - Dinamiche Aziendali srl
# Copyright 2022 Simone Rubino - TAKOBI

from odoo import api, fields, models
from odoo.exceptions import Warning as UserError
from odoo.tools.translate import _


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.multi
    def _set_rc_flag(self, invoice):
        self.ensure_one()
        if invoice.type in ['in_invoice', 'in_refund']:
            fposition = invoice.fiscal_position_id
            self.rc = bool(fposition.rc_type_id)

    @api.onchange('invoice_line_tax_ids')
    def onchange_invoice_line_tax_id(self):
        self._set_rc_flag(self.invoice_id)

    rc = fields.Boolean("RC")

    def _set_additional_fields(self, invoice):
        res = super(AccountInvoiceLine, self)._set_additional_fields(invoice)
        self._set_rc_flag(invoice)
        return res


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

    @api.onchange('fiscal_position_id')
    def onchange_rc_fiscal_position_id(self):
        for line in self.invoice_line_ids:
            line._set_rc_flag(self)

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        res = super(AccountInvoice, self)._onchange_partner_id()
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
            'product_id': line.product_id.id,
            'name': line.name,
            'uom_id': line.product_id.uom_id.id,
            'price_unit': line.price_unit,
            'quantity': line.quantity,
            'discount': line.discount,
            }

    def rc_inv_vals(self, partner, account, rc_type, lines, currency):
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
            supplier.display_name, self.reference or '', self.date,
            self.number
        )
        return {
            'partner_id': partner.id,
            'type': type,
            'account_id': account.id,
            'journal_id': rc_type.journal_id.id,
            'invoice_line_ids': lines,
            'date_invoice': self.date,
            'date': self.date,
            'origin': self.number,
            'rc_purchase_invoice_id': self.id,
            'name': rc_type.self_invoice_text,
            'currency_id': currency.id,
            'fiscal_position_id': False,
            'payment_term_id': False,
            'comment': comment,
            }

    def get_inv_line_to_reconcile(self):
        for inv_line in self.move_id.line_ids:
            if (self.type == 'in_invoice') and inv_line.credit:
                return inv_line
            elif (self.type == 'in_refund') and inv_line.debit:
                return inv_line
        return False

    def get_rc_inv_line_to_reconcile(self, invoice):
        for inv_line in invoice.move_id.line_ids:
            if (invoice.type == 'out_invoice') and inv_line.debit:
                return inv_line
            elif (invoice.type == 'out_refund') and inv_line.credit:
                return inv_line
        return False

    def rc_payment_vals(self, rc_type):
        return {
            'journal_id': rc_type.payment_journal_id.id,
            # 'period_id': self.period_id.id,
            'date': self.date,
            }

    def compute_rc_amount_tax(self):
        rc_amount_tax = 0.0
        round_curr = self.currency_id.round
        rc_lines = self.invoice_line_ids.filtered(lambda l: l.rc)
        for rc_line in rc_lines:
            price_unit = \
                rc_line.price_unit * (1 - (rc_line.discount or 0.0) / 100.0)
            taxes = rc_line.invoice_line_tax_ids.compute_all(
                price_unit,
                self.currency_id,
                rc_line.quantity,
                product=rc_line.product_id,
                partner=rc_line.partner_id)['taxes']
            rc_amount_tax += sum([tax['amount'] for tax in taxes])

        # convert the amount to main company currency, as
        # compute_rc_amount_tax is used for debit/credit fields
        invoice_currency = self.currency_id.with_context(
            date=self.date_invoice)
        main_currency = self.company_currency_id.with_context(
            date=self.date_invoice)
        if invoice_currency != main_currency:
            round_curr = main_currency.round
            rc_amount_tax = invoice_currency.compute(
                rc_amount_tax, main_currency)

        return round_curr(rc_amount_tax)

    def rc_credit_line_vals(self, journal):
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
            }

    def rc_debit_line_vals(self, amount=None):
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
            'partner_id': self.partner_id.id,
            }

    def rc_invoice_payment_vals(self, rc_type):
        return {
            'journal_id': rc_type.payment_journal_id.id,
            # 'period_id': self.period_id.id,
            'date': self.date,
            }

    def rc_payment_credit_line_vals(self, invoice):
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
            'partner_id': invoice.partner_id.id,
            }

    def rc_payment_debit_line_vals(self, invoice, journal):
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
            }

    def reconcile_supplier_invoice(self):
        rc_type = self.fiscal_position_id.rc_type_id

        move_model = self.env['account.move']
        move_line_model = self.env['account.move.line']

        rc_payment_data = self.rc_payment_vals(rc_type)
        rc_invoice = self.rc_self_invoice_id
        payment_credit_line_data = self.rc_payment_credit_line_vals(
            rc_invoice)
        payment_debit_line_data = self.rc_debit_line_vals(
            payment_credit_line_data['credit'])
        rc_payment_data['line_ids'] = [
            (0, 0, payment_debit_line_data),
            (0, 0, payment_credit_line_data),
        ]
        rc_payment = move_model.create(rc_payment_data)
        for move_line in rc_payment.line_ids:
            if move_line.debit:
                payment_debit_line = move_line
            elif move_line.credit:
                payment_credit_line = move_line
        rc_payment.post()

        lines_to_rec = move_line_model.browse([
            self.get_inv_line_to_reconcile().id,
            payment_debit_line.id
        ])
        lines_to_rec.reconcile()

        rc_lines_to_rec = move_line_model.browse([
            self.get_rc_inv_line_to_reconcile(rc_invoice).id,
            payment_credit_line.id
        ])
        rc_lines_to_rec.reconcile()

    def partially_reconcile_supplier_invoice(self, rc_payment):
        move_line_model = self.env['account.move.line']
        payment_debit_line = None
        for move_line in rc_payment.line_ids:
            if move_line.account_id.internal_type == 'payable' and (
                    move_line.debit or move_line.credit):
                payment_debit_line = move_line
                break
        if payment_debit_line:
            inv_lines_to_rec = move_line_model.browse(
                [self.get_inv_line_to_reconcile().id,
                    payment_debit_line.id])
            inv_lines_to_rec.reconcile()

    def reconcile_rc_invoice(self):
        rc_type = self.fiscal_position_id.rc_type_id
        move_model = self.env['account.move']
        rc_payment_data = self.rc_payment_vals(rc_type)
        payment_credit_line_data = self.rc_credit_line_vals(
            rc_type.payment_journal_id)
        payment_debit_line_data = self.rc_debit_line_vals()
        rc_invoice = self.rc_self_invoice_id
        rc_payment_credit_line_data = self.rc_payment_credit_line_vals(
            rc_invoice)
        rc_payment_debit_line_data = self.rc_payment_debit_line_vals(
            rc_invoice, rc_type.payment_journal_id)
        rc_payment_data['line_ids'] = [
            (0, 0, payment_debit_line_data),
            (0, 0, payment_credit_line_data),
            (0, 0, rc_payment_debit_line_data),
            (0, 0, rc_payment_credit_line_data),
        ]
        rc_payment = move_model.create(rc_payment_data)

        move_line_model = self.env['account.move.line']
        rc_payment.post()
        inv_line_to_reconcile = self.get_rc_inv_line_to_reconcile(rc_invoice)
        for move_line in rc_payment.line_ids:
            if move_line.account_id.id == inv_line_to_reconcile.account_id.id:
                rc_payment_line_to_reconcile = move_line

        rc_lines_to_rec = move_line_model.browse(
            [inv_line_to_reconcile.id,
                rc_payment_line_to_reconcile.id])
        rc_lines_to_rec.reconcile()
        return rc_payment

    def generate_self_invoice(self):
        rc_type = self.fiscal_position_id.rc_type_id
        if not rc_type.payment_journal_id.default_credit_account_id:
            raise UserError(
                _('There is no default credit account defined \n'
                  'on journal "%s".') % rc_type.payment_journal_id.name)
        if rc_type.partner_type == 'other':
            rc_partner = rc_type.partner_id
        else:
            rc_partner = self.partner_id
        rc_currency = self.currency_id
        rc_account = rc_partner.property_account_receivable_id

        rc_invoice_lines = []
        for line in self.invoice_line_ids:
            if line.rc:
                rc_invoice_line = self.rc_inv_line_vals(line)
                line_tax_ids = line.invoice_line_tax_ids
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
                    rc_invoice_line['invoice_line_tax_ids'] = [
                        (6, False, mapped_taxes.ids)]
                rc_invoice_line[
                    'account_id'] = rc_type.transitory_account_id.id
                rc_invoice_lines.append([0, False, rc_invoice_line])
        if rc_invoice_lines:
            inv_vals = self.rc_inv_vals(
                rc_partner, rc_account, rc_type, rc_invoice_lines, rc_currency)

            # create or write the self invoice
            if self.rc_self_invoice_id:
                # this is needed when user takes back to draft supplier
                # invoice, edit and validate again
                rc_invoice = self.rc_self_invoice_id
                rc_invoice.invoice_line_ids.unlink()
                rc_invoice.period_id = False
                rc_invoice.write(inv_vals)
                rc_invoice.compute_taxes()
            else:
                rc_invoice = self.create(inv_vals)
                self.rc_self_invoice_id = rc_invoice.id
            rc_invoice.action_invoice_open()

            if self.amount_total:
                # No need to reconcile invoices with total = 0
                if rc_type.with_supplier_self_invoice:
                    self.reconcile_supplier_invoice()
                else:
                    rc_payment = self.reconcile_rc_invoice()
                    self.partially_reconcile_supplier_invoice(rc_payment)

    def generate_supplier_self_invoice(self):
        rc_type = self.fiscal_position_id.rc_type_id
        if not self.rc_self_purchase_invoice_id:
            supplier_invoice = self.copy()
        else:
            supplier_invoice_vals = self.copy_data()
            supplier_invoice = self.rc_self_purchase_invoice_id
            supplier_invoice.invoice_line_ids.unlink()
            supplier_invoice.write(supplier_invoice_vals[0])

        supplier_invoice.partner_bank_id = None

        # because this field has copy=False
        supplier_invoice.date = self.date
        supplier_invoice.date_invoice = self.date
        supplier_invoice.date_due = self.date
        supplier_invoice.partner_id = rc_type.partner_id.id
        supplier_invoice.journal_id = rc_type.supplier_journal_id.id
        for inv_line in supplier_invoice.invoice_line_ids:
            line_tax_ids = inv_line.invoice_line_tax_ids
            mapped_taxes = rc_type.map_tax(
                line_tax_ids,
                'original_purchase_tax_id',
                'purchase_tax_id',
            )
            if line_tax_ids and mapped_taxes:
                inv_line.invoice_line_tax_ids = [
                    (6, False, mapped_taxes.ids),
                ]

            inv_line.account_id = rc_type.transitory_account_id.id
        self.rc_self_purchase_invoice_id = supplier_invoice.id

        # temporary disabling self invoice automations
        supplier_invoice.fiscal_position_id = None
        supplier_invoice.compute_taxes()
        supplier_invoice.check_total = supplier_invoice.amount_total
        supplier_invoice.action_invoice_open()
        supplier_invoice.fiscal_position_id = self.fiscal_position_id.id

    @api.multi
    def invoice_validate(self):
        res = super(AccountInvoice, self).invoice_validate()
        for invoice in self:
            fp = invoice.fiscal_position_id
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
                      "defined in fiscal position {fp}, is not managed yet")
                    .format(fp=fp.display_name))
        return res

    def remove_rc_payment(self):
        inv = self
        if inv.rc_self_invoice_id.payment_move_line_ids:
            if len(inv.rc_self_invoice_id.payment_move_line_ids) > 1:
                raise UserError(
                    _('There are more than one payment line.\n'
                      'In that case account entries cannot be canceled'
                      'automatically. Please proceed manually'))
            payment_move = inv.rc_self_invoice_id.payment_move_line_ids[0].\
                move_id

            # remove move reconcile related to the supplier invoice
            move = inv.move_id
            rec_partial = move.mapped('line_ids').filtered(
                'matched_debit_ids').mapped('matched_debit_ids')
            rec_partial_lines = (
                rec_partial.mapped('credit_move_id') |
                rec_partial.mapped('debit_move_id')
            )
            rec_partial_lines.remove_move_reconcile()

            # also remove full reconcile, in case of with_supplier_self_invoice
            rec_partial_lines = move.mapped('line_ids').filtered(
                'full_reconcile_id'
            ).mapped('full_reconcile_id.reconciled_line_ids')
            rec_partial_lines.remove_move_reconcile()
            # remove move reconcile related to the self invoice
            move = inv.rc_self_invoice_id.move_id
            rec_lines = move.mapped('line_ids').filtered(
                'full_reconcile_id'
            ).mapped('full_reconcile_id.reconciled_line_ids')
            rec_lines.remove_move_reconcile()
            # invalidate and delete the payment move generated
            # by the self invoice creation
            payment_move.button_cancel()
            payment_move.unlink()

        # cancel self invoice
        self_invoice = self.browse(
            inv.rc_self_invoice_id.id)
        self_invoice.action_invoice_cancel()

    @api.multi
    def action_cancel(self):
        for inv in self:
            rc_type = inv.fiscal_position_id.rc_type_id
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
                inv.rc_self_purchase_invoice_id.action_invoice_cancel()
        return super(AccountInvoice, self).action_cancel()

    @api.multi
    def action_invoice_draft(self):
        new_self = self.with_context(rc_set_to_draft=True)
        super(AccountInvoice, new_self).action_invoice_draft()
        invoice_model = new_self.env['account.invoice']
        for inv in new_self:
            if inv.rc_self_invoice_id:
                self_invoice = invoice_model.browse(
                    inv.rc_self_invoice_id.id)
                self_invoice.action_invoice_draft()
            if inv.rc_self_purchase_invoice_id:
                self_purchase_invoice = invoice_model.browse(
                    inv.rc_self_purchase_invoice_id.id)
                self_purchase_invoice.action_invoice_draft()
        return True

    def get_tax_amount_added_for_rc(self):
        res = 0
        for line in self.invoice_line_ids:
            if line.rc:
                price_unit = line.price_unit * (
                    1 - (line.discount or 0.0) / 100.0)
                taxes = line.invoice_line_tax_ids.compute_all(
                    price_unit, self.currency_id, line.quantity,
                    line.product_id, self.partner_id)['taxes']
                for tax in taxes:
                    res += tax['amount']
        return res
