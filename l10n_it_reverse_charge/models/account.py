# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Abstract (http://www.abstract.it)
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

from openerp import fields, models
from openerp.tools.translate import _
from openerp import netsvc
from openerp.exceptions import Warning


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    rc_tax_ids = fields.One2many(
        'account.fiscal.position.rc.tax',
        'position_id',
        string='RC Tax Mapping')
    rc_journal_id = fields.Many2one(
        'account.journal', string='RC Payment Journal')
    reverse_charge_vat = fields.Boolean("Reverse Charge VAT")


class AccountFiscalPositionRCTax(models.Model):
    _name = 'account.fiscal.position.rc.tax'
    _description = 'Taxes Fiscal Position for Reverse Charge Operations'
    _rec_name = 'position_id'

    position_id = fields.Many2one(
        'account.fiscal.position',
        string='Fiscal Position',
        required=True,
        ondelete='cascade')
    tax_src_id = fields.Many2one(
        'account.tax',
        string='Tax Source',
        required=True)
    tax_dest_id = fields.Many2one(
        'account.tax',
        string='Replacement Tax')

    _sql_constraints = [
        ('tax_src_dest_uniq',
         'unique (position_id,tax_src_id,tax_dest_id)',
         'A tax fiscal position could be defined only once time on same\
         taxes.')
    ]


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    rc_sale_invoice_id = fields.Many2one(
        'account.invoice',
        string='Reverse Charge Sale Invoice')
    rc_purchase_invoice_id = fields.Many2one(
        'account.invoice',
        string='Reverse Charge Purchase Invoice')
    rc_purchase_invoice_partner_id = fields.Many2one(
        'res.partner',
        related='rc_purchase_invoice_id.partner_id',
        string='Reverse Charge Invoice Partner')

    def copy(self, cr, uid, ids, default=None, context=None):
        if not context:
            context = {}
        if not default:
            default = {}
        default.update({'rc_sale_invoice_id': False})
        default.update({'rc_purchase_invoice_id': False})
        return super(AccountInvoice, self).copy(
            cr, uid, ids, default=default, context=context)

    def invoice_validate(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        res = super(AccountInvoice, self).invoice_validate(
            cr, uid, ids, context)

        invoice_obj = self.pool.get('account.invoice')
        user_obj = self.pool.get('res.users')
        move_obj = self.pool.get('account.move')
        move_line_obj = self.pool.get('account.move.line')

        company = user_obj.browse(cr, uid, uid).company_id
        rc_partner = company.rc_partner_id

        for invoice in invoice_obj.browse(cr, uid, ids):
            rc_invoice_lines = []
            for line in invoice.invoice_line:
                if line.reverse_charge_vat:
                    if rc_partner:
                        rc_partner_id = rc_partner.id
                        rc_account = rc_partner.property_account_receivable
                        rc_account_id = rc_account.id
                    else:
                        raise Warning(
                            _('Reverse Charge default partner not configured.'))
                    rc_invoice_line = {
                        'product_id': line.product_id.id,
                        'name': line.name,
                        'uom_id': line.uos_id.id,
                        'price_unit': line.price_unit,
                        'quantity': line.quantity,
                        }
                    line_tax = line.invoice_line_tax_id
                    if line_tax:
                        tax_code_id = False
                        if (invoice.fiscal_position and
                                invoice.fiscal_position.rc_tax_ids):
                            fiscal_position = invoice.fiscal_position
                            for tax_mapping in fiscal_position.rc_tax_ids:
                                if tax_mapping.tax_src_id == line_tax[0]:
                                    tax_code_id = tax_mapping.tax_dest_id.id
                        if tax_code_id:
                            rc_invoice_line['invoice_line_tax_id'] = [
                                (6, False, [tax_code_id])]
                    if company.rc_transitory_account_id:
                        account_id = company.rc_transitory_account_id.id
                        rc_invoice_line['account_id'] = account_id
                    rc_invoice_lines.append([0, False, rc_invoice_line])

            if rc_invoice_lines:
                if invoice.rc_sale_invoice_id:
                    raise Warning(_('Related sale invoice already set.'))
                if invoice.rc_purchase_invoice_id:
                    raise Warning(_('Related purchase invoice already set.'))
                else:
                    invoice_data = {
                        'partner_id': rc_partner_id,
                        'type': 'out_invoice',
                        'account_id': rc_account_id,
                        'journal_id': company.rc_journal_id.id,
                        'rc_purchase_invoice_id': invoice.id,
                        'invoice_line': rc_invoice_lines,
                        'vat_on_payment': False,
                        'date_invoice': invoice.registration_date,
                        'registration_date': invoice.registration_date,
                        'payment_term': 1,
                        'origin': invoice.number,
                        'name': '--',
                    }
                    new_invoice_id = invoice_obj.create(cr, uid, invoice_data)
                    wf_service = netsvc.LocalService("workflow")
                    wf_service.trg_validate(
                        uid, 'account.invoice', new_invoice_id, 'invoice_open',
                        cr)
                    invoice.write({'rc_sale_invoice_id': new_invoice_id})

                rc_payment_journal = company.rc_payment_journal_id
                rc_payment_sequence = rc_payment_journal.sequence_id
                if not rc_payment_sequence and not rc_payment_sequence.active:
                    raise Warning(
                        _('Please activate the sequence of selected journal!'))

                ## partially reconcile purchase invoice

                rc_payment_move = {
                    'journal_id': rc_payment_journal.id,
                    'period_id': invoice.period_id.id,
                    'date': invoice.registration_date,
                }
                rc_payment_move_id = move_obj.create(
                    cr, uid, rc_payment_move, context=context)

                inv_line_to_reconcile = False
                rc_inv_line = False
                for inv_line in invoice.move_id.line_id:
                    if inv_line.credit:
                        inv_line_to_reconcile = inv_line

                amount_tax = invoice.amount_tax

                payment_credit_line_data = {
                    'name': invoice.number,
                    'credit': amount_tax,
                    'debit': 0.0,
                    'account_id': (
                        rc_payment_journal.default_credit_account_id.id),
                    'move_id': rc_payment_move_id,
                }
                move_line_obj.create(
                    cr, uid, payment_credit_line_data, context=context)

                payment_line_to_reconcile_data = {
                    'name': invoice.number,
                    'debit': amount_tax,
                    'credit': 0.0,
                    'account_id': inv_line_to_reconcile.account_id.id,
                    'move_id': rc_payment_move_id,
                    'partner_id': invoice.partner_id.id,
                }
                payment_line_to_reconcile_id = move_line_obj.create(
                    cr, uid, payment_line_to_reconcile_data, context=context)

                move_line_obj.reconcile_partial(
                    cr, uid,
                    [inv_line_to_reconcile.id, payment_line_to_reconcile_id],
                    context=context)

                ## reconcile rc invoice

                rc_invoice = invoice_obj.browse(
                    cr, uid, new_invoice_id, context=context)

                rc_inv_payment_move = {
                    'journal_id': rc_payment_journal.id,
                    'period_id': rc_invoice.period_id.id,
                    'date': rc_invoice.registration_date,
                }
                rc_inv_payment_move_id = move_obj.create(
                    cr, uid, rc_inv_payment_move, context=context)

                rc_inv_line_to_reconcile = False
                for inv_line in rc_invoice.move_id.line_id:
                    if inv_line.debit:
                        rc_inv_line_to_reconcile = inv_line

                payment_line_to_reconcile_data = {
                    'name': rc_invoice.number,
                    'credit': rc_inv_line_to_reconcile.debit,
                    'debit': 0.0,
                    'account_id': rc_inv_line_to_reconcile.account_id.id,
                    'move_id': rc_inv_payment_move_id,
                    'partner_id': rc_invoice.partner_id.id,
                }
                payment_line_to_reconcile_id = move_line_obj.create(
                    cr, uid, payment_line_to_reconcile_data, context=context)

                payment_debit_line_data = {
                    'name': rc_invoice.number,
                    'debit': rc_inv_line_to_reconcile.debit,
                    'credit': 0.0,
                    'account_id': (
                        rc_payment_journal.default_credit_account_id.id),
                    'move_id': rc_inv_payment_move_id,
                }
                move_line_obj.create(
                    cr, uid, payment_debit_line_data, context=context)

                move_line_obj.reconcile_partial(
                    cr, uid,
                    [rc_inv_line_to_reconcile.id, payment_line_to_reconcile_id],
                    context=context)

        return res


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    reverse_charge_vat = fields.Boolean("RC")

    def onchange_tax(self, cr, uid, ids, tax, fp_id, context=None):
        if not context:
            context = {}
        values = {}
        fp_obj = self.pool.get('account.fiscal.position')
        if fp_id and tax and tax[0][2]:
            fp = fp_obj.browse(cr, uid, fp_id)
            for tax_pos in fp.rc_tax_ids:
                if tax_pos.tax_src_id.id == tax[0][2][0]:
                    values['reverse_charge_vat'] = True
        return {'value': values}


class AccountVoucher(models.Model):
    _inherit = "account.voucher"

    def onchange_writeoff_amount(
            self, cr, uid, ids, line_dr_ids, context=None):
        if not context:
            context = {}
        values = {}
        invoice_pool = self.pool.get('account.invoice')
        user_pool = self.pool.get('res.users')
        user = user_pool.browse(cr, uid, uid)
        company = user.company_id
        rc = False
        for line in line_dr_ids:
            if line[2] and line[2].get('move_line_id', False):
                inv_ids = invoice_pool.search(
                    cr, uid, [
                        ('move_id', '=', line[2].get('move_line_id.id'))])
                if inv_ids:
                    for inv in invoice_pool.browse(cr, uid, inv_ids):
                        for line in inv.invoice_line:
                            if line.reverse_charge_vat:
                                rc = True
        if rc:
            values['payment_option'] = 'with_writeoff'
            values['writeoff_acc_id'] = company.rc_transitory_account_id.id

        return {'value': values}
