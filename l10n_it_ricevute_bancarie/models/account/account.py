# -*- coding: utf-8 -*-
# Copyright (C) 2012 Andrea Cometa.
# Email: info@andreacometa.it
# Web site: http://www.andreacometa.it
# Copyright (C) 2012 Associazione OpenERP Italia
# (<http://www.odoo-italia.org>).
# Copyright (C) 2012-2017 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import Warning as UserError


class AccountPaymentTerm(models.Model):
    # flag riba utile a distinguere la modalità di pagamento
    _inherit = 'account.payment.term'

    riba = fields.Boolean('Riba', default=False)
    riba_payment_cost = fields.Float(
        'RiBa Payment Cost', digits=dp.get_precision('Account'),
        help="Collection fees amount. If different from 0, "
             "for each payment deadline an invoice line will be added "
             "to invoice, with this amount"
    )


class ResBankAddField(models.Model):
    _inherit = 'res.bank'
    banca_estera = fields.Boolean('Banca Estera')


class ResPartnerBankAdd(models.Model):
    _inherit = 'res.partner.bank'
    codice_sia = fields.Char(
        "SIA Code", size=5,
        help="Identification Code of the Company in the System Interbank")


# se distinta_line_ids == None allora non è stata emessa
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    distinta_line_ids = fields.One2many(
        'riba.distinta.move.line', 'move_line_id', "Dettaglio riba")
    riba = fields.Boolean(
        related='invoice_id.payment_term_id.riba', string='RiBa', store=False)
    unsolved_invoice_ids = fields.Many2many(
        'account.invoice', 'invoice_unsolved_line_rel', 'line_id',
        'invoice_id', 'Unsolved Invoices')
    iban = fields.Char(
        related='partner_id.bank_ids.acc_number', string='IBAN', store=False)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        model_data_obj = self.env['ir.model.data']
        ids = model_data_obj.search([
            ('module', '=', 'l10n_it_ricevute_bancarie'),
            ('name', '=', 'view_riba_da_emettere_tree')])
        if ids:
            view_payments_tree_id = model_data_obj.get_object_reference(
                'l10n_it_ricevute_bancarie', 'view_riba_da_emettere_tree')
        if ids and view_id == view_payments_tree_id[1]:
            # Use RiBa list
            result = super(models.Model, self).fields_view_get(
                view_id, view_type, toolbar=toolbar, submenu=submenu)
        else:
            # Use special views for account.move.line object
            # (for ex. tree view contains user defined fields)
            result = super(AccountMoveLine, self).fields_view_get(
                view_id, view_type, toolbar=toolbar, submenu=submenu)
        return result

    def get_riba_lines(self):
        riba_lines = self.env['riba.distinta.line']
        return riba_lines.search([
            ('acceptance_move_id', '=', self.move_id.id)
        ])

    def update_paid_riba_lines(self):
        # set paid only if not unsolved
        if not self.env.context.get('unsolved_reconciliation'):
            riba_lines = self.get_riba_lines()
            for riba_line in riba_lines:
                # allowed transitions:
                # accredited_to_paid and accepted_to_paid. See workflow
                if riba_line.state in ['confirmed', 'accredited']:
                    if riba_line.test_reconciled():
                        riba_line.state = 'paid'
                        riba_line.distinta_id.signal_workflow('paid')

    @api.multi
    def reconcile(
        self, writeoff_acc_id=False, writeoff_journal_id=False
    ):
        res = super(AccountMoveLine, self).reconcile(
            writeoff_acc_id=writeoff_acc_id,
            writeoff_journal_id=writeoff_journal_id)
        for line in self:
            line.update_paid_riba_lines()
        return res


class AccountInvoice(models.Model):

    @api.multi
    @api.depends(
        'unsolved_move_line_ids.unsolved_invoice_ids',
        'unsolved_move_line_ids.full_reconcile_id',
        'unsolved_move_line_ids.matched_debit_ids',
        'unsolved_move_line_ids.matched_credit_ids'
    )
    def _compute_is_unsolved(self):
        for invoice in self:
            invoice.is_unsolved = False
            reconciled_unsolved = 0
            for unsolved_move_line in invoice.unsolved_move_line_ids:
                if unsolved_move_line.reconciled:
                    reconciled_unsolved += 1
            if len(invoice.unsolved_move_line_ids) != reconciled_unsolved:
                invoice.is_unsolved = True

    _inherit = "account.invoice"
    unsolved_move_line_ids = fields.Many2many(
        'account.move.line', 'invoice_unsolved_line_rel', 'invoice_id',
        'line_id', 'Unsolved journal items')
    is_unsolved = fields.Boolean(
        "The unsolved is open", compute="_compute_is_unsolved", store=True
    )

    def month_check(self, invoice_date_due, all_date_due):
        """
        :param invoice_date_due: first date due of invoice
        :param all_date_due: list of date of dues for partner
        :return: True if month of invoice_date_due is in a list of all_date_due
        """
        for d in all_date_due:
            if invoice_date_due[:7] == d[:7]:
                return True
        return False

    @api.multi
    def action_move_create(self):
        for invoice in self:
            # ---- Add a line with payment cost for each due only for fist due
            # ---- of the month
            if (
                invoice.type != 'out_invoice' or not
                invoice.payment_term_id or not
                invoice.payment_term_id.riba or
                invoice.payment_term_id.riba_payment_cost == 0.0
            ):
                continue
            if not invoice.company_id.due_cost_service_id:
                raise UserError(
                    _('Set a Service for Due Cost in Company Config'))
            # ---- Apply Due Cost on invoice only on first due of the month
            # ---- Get Date of first due
            move_line = self.env['account.move.line'].search([
                ('partner_id', '=', invoice.partner_id.id)])
            # ---- Filtered recordset with date_maturity
            move_line = move_line.filtered(
                lambda l: l.date_maturity is not False)
            # ---- Sorted
            move_line = move_line.sorted(key=lambda r: r.date_maturity)
            # ---- Get date
            previous_date_due = move_line.mapped('date_maturity')
            pterm = self.env['account.payment.term'].browse(
                self.payment_term_id.id)
            pterm_list = pterm.compute(value=1, date_ref=self.date_invoice)
            for pay_date in pterm_list[0]:
                if not self.month_check(pay_date[0], previous_date_due):
                    # ---- Get Line values for service product
                    service_prod = invoice.company_id.due_cost_service_id
                    line_obj = self.env['account.invoice.line']
                    account = (
                        service_prod.product_tmpl_id.get_product_accounts(
                            invoice.fiscal_position_id)['income']
                    )
                    line_vals = {
                        'product_id': service_prod.id,
                        'uom_id': service_prod.uom_id.id,
                        'invoice_id': invoice.id,
                        'price_unit': (
                            invoice.payment_term_id.riba_payment_cost),
                        'due_cost_line': True,
                        'name': _('{line_name} for {month}-{year}').format(
                            line_name=service_prod.name,
                            month=pay_date[0][5:7],
                            year=pay_date[0][:4],
                        ),
                        'account_id': account.id,
                    }
                    # ---- Update Line Value with tax if is set on product
                    if invoice.company_id.due_cost_service_id.taxes_id:
                        tax = invoice.company_id.due_cost_service_id.taxes_id
                        line_vals.update({
                            'invoice_line_tax_ids': [(4, tax.id)]
                        })
                    line_obj.create(line_vals)
                    # ---- recompute invoice taxes
                    invoice.compute_taxes()
        super(AccountInvoice, self).action_move_create()

    @api.multi
    def action_invoice_draft(self):
        # ---- Delete Due Cost Line of invoice when set Back to Draft
        # ---- line was added on new validate
        for invoice in self:
            for line in invoice.invoice_line_ids:
                if line.due_cost_line:
                    line.unlink()
        super(AccountInvoice, self).action_invoice_draft()

    @api.multi
    def action_cancel(self):
        for invoice in self:
            # we get move_lines with date_maturity and check if they are
            # present in some riba_distinta_line
            move_line_model = self.env['account.move.line']
            rdml_model = self.env['riba.distinta.move.line']
            move_line_ids = move_line_model.search([
                ('move_id', '=', invoice.move_id.id),
                ('date_maturity', '!=', False)])
            if move_line_ids:
                riba_line_ids = rdml_model.search(
                    [('move_line_id', 'in', [m.id for m in move_line_ids])])
                if riba_line_ids:
                    if len(riba_line_ids) > 1:
                        riba_line_ids = riba_line_ids[0]
                    raise UserError(
                        _('Invoice is linked to RI.BA. list nr {riba}').format(
                            riba=riba_line_ids.riba_line_id.distinta_id.name
                        ))
        super(AccountInvoice, self).action_cancel()

    def copy(self, default=None):
        self.ensure_one()
        # Delete Due Cost Line of invoice when copying
        invoice = super(AccountInvoice, self).copy(default)
        if invoice:
            for line in invoice.invoice_line_ids:
                if line.due_cost_line:
                    line.unlink()


class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'
    due_cost_line = fields.Boolean('RiBa Due Cost Line')


class AccountFullReconcile(models.Model):
    _inherit = 'account.full.reconcile'

    def get_riba_lines(self):
        riba_lines = self.env['riba.distinta.line']
        for move_line in self.reconciled_line_ids:
            riba_lines |= riba_lines.search([
                ('acceptance_move_id', '=', move_line.move_id.id)
            ])
        return riba_lines

    def unreconcile_riba_lines(self, riba_lines):
        for riba_line in riba_lines:
            # allowed transitions:
            # paid_to_cancel and unsolved_to_cancel. See workflow
            if riba_line.state in ['paid', 'unsolved']:
                if not riba_line.test_reconciled():
                    if riba_line.distinta_id.accreditation_move_id:
                        riba_line.state = 'accredited'
                        riba_line.distinta_id.signal_workflow('accredited')
                    else:
                        riba_line.state = 'confirmed'
                        riba_line.distinta_id.signal_workflow('accepted')

    @api.multi
    def unlink(self):
        riba_lines = None
        for rec in self:
            riba_lines = rec.get_riba_lines()
        res = super(AccountFullReconcile, self).unlink()
        if riba_lines:
            self.unreconcile_riba_lines(riba_lines)
        return res


class AccountPartialReconcile(models.Model):
    _inherit = 'account.partial.reconcile'

    @api.multi
    def unlink(self):
        riba_lines = None
        for rec in self:
            riba_lines = rec.get_riba_lines()
        res = super(AccountPartialReconcile, self).unlink()
        if riba_lines:
            self.env['account.full.reconcile'].unreconcile_riba_lines(
                riba_lines)
        return res

    def get_riba_lines(self):
        riba_lines = self.env['riba.distinta.line']
        riba_lines |= riba_lines.search([
            ('acceptance_move_id', '=', self.debit_move_id.move_id.id)
        ])
        riba_lines |= riba_lines.search([
            ('acceptance_move_id', '=', self.credit_move_id.move_id.id)
        ])
        return riba_lines
