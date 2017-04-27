# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2012 Andrea Cometa.
#    Email: info@andreacometa.it
#    Web site: http://www.andreacometa.it
#    Copyright (C) 2012-2015 Lorenzo Battistini - Agile Business Group
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    Copyright (C) 2012 Associazione OpenERP Italia
#    (<http://www.odoo-italia.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, orm
from openerp import api, _, models
from openerp.exceptions import Warning as UserError
import openerp.addons.decimal_precision as dp


class AccountPaymentTerm(orm.Model):
    # flag riba utile a distinguere la modalità di pagamento
    _inherit = 'account.payment.term'

    _columns = {
        'riba': fields.boolean('Riba'),
        'riba_payment_cost': fields.float(
            'RiBa Payment Cost', digits_compute=dp.get_precision('Account'),
            help="Collection fees amount. If different from 0, "
                 "for each payment deadline an invoice line will be added "
                 "to invoice, with this amount"),
    }


class ResBankAddField(orm.Model):
    _inherit = 'res.bank'
    _columns = {
        'banca_estera': fields.boolean('Banca Estera'),
    }


class ResPartnerBankAdd(orm.Model):
    _inherit = 'res.partner.bank'
    _columns = {
        'codice_sia': fields.char(
            'Codice SIA', size=5,
            help="Identification Code of the Company in the System Interbank")
    }


# se distinta_line_ids == None allora non è stata emessa
class AccountMoveLine(orm.Model):
    _inherit = "account.move.line"

    _columns = {
        'distinta_line_ids': fields.one2many(
            'riba.distinta.move.line', 'move_line_id', "Dettaglio riba"),
        'riba': fields.related(
            'invoice', 'payment_term', 'riba', type='boolean', string='RiBa',
            store=False),
        'unsolved_invoice_ids': fields.many2many(
            'account.invoice', 'invoice_unsolved_line_rel', 'line_id',
            'invoice_id', 'Unsolved Invoices'),
        'iban': fields.related(
            'partner_id', 'bank_ids', 'iban', type='char', string='IBAN',
            store=False),
    }
    _defaults = {
        'distinta_line_ids': None,
    }

    def fields_view_get(
        self, cr, uid, view_id=None, view_type='form',
        context=None, toolbar=False, submenu=False
    ):
        # Special view for account.move.line object
        # (for ex. tree view contains user defined fields)
        result = super(AccountMoveLine, self).fields_view_get(
            cr, uid, view_id, view_type, context=context, toolbar=toolbar,
            submenu=submenu)
        try:
            view_payments_tree_id = self.pool.get(
                'ir.model.data').get_object_reference(
                cr, uid, 'l10n_it_ricevute_bancarie',
                'view_riba_da_emettere_tree')
        except ValueError:
            return result
        if view_id == view_payments_tree_id[1]:
            # Use RiBa list - grazie a eLBati @ account_due_list
            return super(orm.Model, self).fields_view_get(
                cr, uid, view_id, view_type, context, toolbar=toolbar,
                submenu=submenu)
        else:
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
                    if riba_line.test_reconcilied():
                        riba_line.state = 'paid'
                        riba_line.distinta_id.signal_workflow('paid')

    @api.multi
    def reconcile(
        self, type='auto', writeoff_acc_id=False,
        writeoff_period_id=False, writeoff_journal_id=False
    ):
        res = super(AccountMoveLine, self).reconcile(
            type=type, writeoff_acc_id=writeoff_acc_id,
            writeoff_period_id=writeoff_period_id,
            writeoff_journal_id=writeoff_journal_id)
        for line in self:
            line.update_paid_riba_lines()
        return res


class AccountInvoice(orm.Model):

    def _get_is_unsolved(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            res[invoice.id] = False
            reconciled_unsolved = 0
            for unsolved_move_line in invoice.unsolved_move_line_ids:
                if unsolved_move_line.reconcile_id:
                    reconciled_unsolved += 1
            if len(invoice.unsolved_move_line_ids) != reconciled_unsolved:
                res[invoice.id] = True
        return res

    def _get_invoice_by_move_line(self, cr, uid, ids, context=None):
        result = []
        for move_line in self.pool['account.move.line'].browse(
            cr, uid, ids, context=context
        ):
            result.extend([i.id for i in move_line.unsolved_invoice_ids])
        return list(set(result))

    _inherit = "account.invoice"
    _columns = {
        'unsolved_move_line_ids': fields.many2many(
            'account.move.line', 'invoice_unsolved_line_rel', 'invoice_id',
            'line_id', 'Unsolved journal items'),
        'is_unsolved': fields.function(
            _get_is_unsolved, type='boolean',
            string="The unsolved is open",
            store={
                'account.invoice': (
                    lambda self, cr, uid, ids, c={}: ids, [
                        'unsolved_move_line_ids'], 10
                ),
                'account.move.line': (_get_invoice_by_move_line, [
                    'unsolved_invoice_ids', 'reconcile_id'], 10),
            }
        ),

    }

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
            if invoice.type != 'out_invoice' or not invoice.payment_term \
                    or not invoice.payment_term.riba \
                    or invoice.payment_term.riba_payment_cost == 0.0:
                continue
            if not invoice.company_id.due_cost_service_id:
                raise UserError('Set a Service for Due Cost in Company Config')
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
                self.payment_term.id)
            pterm_list = pterm.compute(value=1, date_ref=self.date_invoice)
            for pay_date in pterm_list[0]:
                if not self.month_check(pay_date[0], previous_date_due):
                    # ---- Get Line values for service product
                    service_prod = invoice.company_id.due_cost_service_id
                    line_obj = self.env['account.invoice.line']
                    line_vals = line_obj.product_id_change(
                        service_prod.id,
                        service_prod.uom_id.id,
                        partner_id=invoice.partner_id.id,
                        qty=1,
                    )
                    # ---- Update Line Values with product,
                    # ---- invoice and due cost
                    line_vals['value'].update({
                        'product_id': service_prod.id,
                        'invoice_id': invoice.id,
                        'price_unit': invoice.payment_term.riba_payment_cost,
                        'due_cost_line': True,
                        'name': _('{line_name} for {month}-{year}').format(
                            line_name=line_vals['value']['name'],
                            month=pay_date[0][5:7],
                            year=pay_date[0][:4],
                        )
                    })
                    # ---- Update Line Value with tax if is set on product
                    if invoice.company_id.due_cost_service_id.taxes_id:
                        tax = invoice.company_id.due_cost_service_id.taxes_id
                        line_vals['value'].update({
                            'invoice_line_tax_id': [(4, tax.id)]
                        })
                    line_obj.create(line_vals['value'])
                    # ---- recompute invoice taxes
                    invoice.button_reset_taxes()
        super(AccountInvoice, self).action_move_create()

    @api.multi
    def action_cancel_draft(self):
        # ---- Delete Due Cost Line of invoice when set Back to Draft
        # ---- line was added on new validate
        for invoice in self:
            for line in invoice.invoice_line:
                if line.due_cost_line:
                    line.unlink()
        super(AccountInvoice, self).action_cancel_draft()

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
                        _('Attention!'),
                        _('Invoice is linked to RI.BA. list nr {riba}').format(
                            riba=riba_line_ids.riba_line_id.distinta_id.name
                        ))
        super(AccountInvoice, self).action_cancel()

    @api.v7
    @api.one
    def copy(self, default=None):
        # Delete Due Cost Line of invoice when copying
        res = super(AccountInvoice, self).copy(default)
        if res:
            for line in res.invoice_line:
                if line.due_cost_line:
                    line.unlink()


class AccountInvoiceLine(orm.Model):

    _inherit = 'account.invoice.line'

    _columns = {
        'due_cost_line': fields.boolean('RiBa Due Cost Line'),
    }


class AccountMoveReconcile(models.Model):
    _inherit = 'account.move.reconcile'

    def get_riba_lines(self):
        riba_lines = self.env['riba.distinta.line']
        for move_line in self.line_id:
            riba_lines |= riba_lines.search([
                ('acceptance_move_id', '=', move_line.move_id.id)
            ])
        return riba_lines

    def unreconcile_riba_lines(self, riba_lines):
        for riba_line in riba_lines:
            # allowed transitions:
            # paid_to_cancel and unsolved_to_cancel. See workflow
            if riba_line.state in ['paid', 'unsolved']:
                if not riba_line.test_reconcilied():
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
        res = super(AccountMoveReconcile, self).unlink()
        if riba_lines:
            self.unreconcile_riba_lines(riba_lines)
        return res
