# -*- coding: utf-8 -*-
<<<<<<< HEAD:l10n_it_ricevute_bancarie/account/account.py
<<<<<<< HEAD
##############################################################################
#    
=======
#
=======
##############################################################################
>>>>>>> 8fe6aa6... added l10n_it_ricevute_bancarie from 8.0-riba:l10n_it_ricevute_bancarie/models/account/account.py
#
>>>>>>> 20676d5... added l10n_it_ricevute_bancarie from 7.0
#    Copyright (C) 2012 Andrea Cometa.
#    Email: info@andreacometa.it
#    Web site: http://www.andreacometa.it
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    Copyright (C) 2012 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
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
<<<<<<< HEAD:l10n_it_ricevute_bancarie/account/account.py
<<<<<<< HEAD
##############################################################################

from openerp.osv import fields, orm

class account_payment_term(orm.Model):
    # flag riba utile a distinguere la modalità di pagamento
    _inherit = 'account.payment.term'
    
    _columns = {
        'riba' : fields.boolean('Riba'),
=======
#
=======
##############################################################################
>>>>>>> 8fe6aa6... added l10n_it_ricevute_bancarie from 8.0-riba:l10n_it_ricevute_bancarie/models/account/account.py

from openerp.osv import fields, orm
from openerp import api, _
from openerp.exceptions import Warning
import openerp.addons.decimal_precision as dp


class account_payment_term(orm.Model):
    # flag riba utile a distinguere la modalità di pagamento
    _inherit = 'account.payment.term'

    _columns = {
        'riba': fields.boolean('Riba'),
<<<<<<< HEAD
>>>>>>> 20676d5... added l10n_it_ricevute_bancarie from 7.0
=======
        'payment_cost': fields.float(
            'Payment Cost', digits_compute=dp.get_precision('Account'),),
>>>>>>> 67ced3e... [IMP] Management of due cost for Ri.Ba.
    }


class res_bank_add_field(orm.Model):
    _inherit = 'res.bank'
    _columns = {
<<<<<<< HEAD
        'banca_estera' : fields.boolean('Banca Estera'),
=======
        'banca_estera': fields.boolean('Banca Estera'),
>>>>>>> 20676d5... added l10n_it_ricevute_bancarie from 7.0
    }


class res_partner_bank_add(orm.Model):
    _inherit = 'res.partner.bank'
    _columns = {
<<<<<<< HEAD
        'codice_sia' : fields.char('Codice SIA', size=5, help="Identification Code of the Company in the System Interbank")    
=======
        'codice_sia': fields.char(
            'Codice SIA', size=5,
            help="Identification Code of the Company in the System Interbank")
>>>>>>> 20676d5... added l10n_it_ricevute_bancarie from 7.0
    }


# se distinta_line_ids == None allora non è stata emessa
class account_move_line(orm.Model):
    _inherit = "account.move.line"

    _columns = {
<<<<<<< HEAD
        'distinta_line_ids' : fields.one2many('riba.distinta.move.line', 'move_line_id', "Dettaglio riba"),
        'riba': fields.related('invoice', 'payment_term', 'riba', 
            type='boolean', string='RiBa', store=False),
        'unsolved_invoice_ids': fields.many2many('account.invoice', 'invoice_unsolved_line_rel', 'line_id', 'invoice_id', 'Unsolved Invoices'),
        'iban' : fields.related('partner_id', 'bank_ids', 'iban', type='char', string='IBAN', store=False),
    }
    _defaults = {
        'distinta_line_ids' : None,
=======
        'distinta_line_ids': fields.one2many(
            'riba.list.move.line', 'move_line_id', "Dettaglio riba"),
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
>>>>>>> 20676d5... added l10n_it_ricevute_bancarie from 7.0
    }

    def fields_view_get(
        self, cr, uid, view_id=None, view_type='form',
<<<<<<< HEAD
<<<<<<< HEAD:l10n_it_ricevute_bancarie/account/account.py
<<<<<<< HEAD
        context={}, toolbar=False, submenu=False
=======
        context=None, toolbar=False, submenu=False
>>>>>>> 20676d5... added l10n_it_ricevute_bancarie from 7.0
=======
        context={}, toolbar=False, submenu=False
>>>>>>> 8fe6aa6... added l10n_it_ricevute_bancarie from 8.0-riba:l10n_it_ricevute_bancarie/models/account/account.py
=======
        context=None, toolbar=False, submenu=False
>>>>>>> 154323a... fixed errors in tests and added dep needed
    ):
        # Special view for account.move.line object
        # (for ex. tree view contains user defined fields)
        result = super(account_move_line, self).fields_view_get(
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


class account_invoice(orm.Model):
<<<<<<< HEAD
    _inherit = "account.invoice"
    _columns = {
        'unsolved_move_line_ids': fields.many2many('account.move.line', 'invoice_unsolved_line_rel', 'invoice_id', 'line_id', 'Unsolved journal items'),
=======

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
<<<<<<< HEAD
>>>>>>> 20676d5... added l10n_it_ricevute_bancarie from 7.0
=======

>>>>>>> 67ced3e... [IMP] Management of due cost for Ri.Ba.
        }

    def _get_first_date_due(self):
        pterm = self.env['account.payment.term'].browse(self.payment_term.id)
        pterm_list = pterm.compute(value=1, date_ref=self.date_invoice)[0]
        return min(line[0] for line in pterm_list)

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
                    or invoice.payment_term.payment_cost == 0.0:
                continue
            if not invoice.company_id.due_cost_service_id:
                raise Warning('Set a Service for Due Cost in Company Config')
            # ---- Apply Due Cost on invoice only on first due of the month
            # ---- Get Date of first due
            first_date_due = self._get_first_date_due()
            move_line = self.env['account.move.line'].search([
                ('partner_id', '=', invoice.partner_id.id)])
            # ---- Filtered recordset with date_maturity
            move_line = move_line.filtered(
                lambda l: l.date_maturity is not False)
            # ---- Sorted
            move_line = move_line.sorted(key=lambda r: r.date_maturity)
            # ---- Get date
            previous_date_due = move_line.mapped('date_maturity')
            if not self.month_check(first_date_due, previous_date_due):
                # ---- Get Line values for service product
                line_obj = self.env['account.invoice.line']
                line_vals = line_obj.product_id_change(
                    invoice.company_id.due_cost_service_id.id,
                    invoice.company_id.due_cost_service_id.uom_id.id,
                    partner_id=invoice.partner_id.id,
                    qty=1,
                )
                # ---- Update Line Values with product, invoice and due cost
                n_dues = len(invoice.payment_term.line_ids)
                line_vals['value'].update({
                    'product_id': invoice.company_id.due_cost_service_id.id,
                    'invoice_id': invoice.id,
                    'price_unit': invoice.payment_term.payment_cost * n_dues,
                    'due_cost_line': True,
                })
                # ---- Update Line Value with tax if is set on product
                if invoice.company_id.due_cost_service_id.taxes_id:
                    tax = invoice.company_id.due_cost_service_id.taxes_id
                    line_vals['value'].update({
                        'invoice_line_tax_id': [(4, tax.id)]
                    })
                line_obj.create(line_vals['value'])
                # ---- recompute invocie taxes
                invoice.button_reset_taxes()
        super(account_invoice, self).action_move_create()

    @api.multi
    def action_cancel_draft(self):
        # ---- Delete Due Cost Line of invoice when set Back to Draft
        # ---- line was added on new validate
        for invoice in self:
            for line in invoice.invoice_line:
                if line.due_cost_line:
                    line.unlink()
        super(account_invoice, self).action_cancel_draft()


class AccountInvoiceLine(orm.Model):

    _inherit = 'account.invoice.line'

    _columns = {
        'due_cost_line': fields.boolean('Due Cost Line'),
    }
