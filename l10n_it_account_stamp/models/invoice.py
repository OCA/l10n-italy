# -*- coding: utf-8 -*-
##############################################################################
#
#    Italian Localization - Account Stamp
#    See __openerp__.py file for copyright and licensing details.
#
##############################################################################

import openerp.exceptions

from openerp.osv import fields
from openerp.osv.orm import Model

from openerp.tools.translate import _


class account_invoice(Model):
    _inherit = 'account.invoice'

    def _compute_tax_stamp(self, cr, uid, ids, name, args, context=None):
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            res[invoice.id] = self.is_tax_stamp_applicable(
                cr, uid, invoice, context)
        return res

    def _get_stamp_product(self, cr, uid, invoice, context=None):
        stamp_product_id = invoice.company_id.tax_stamp_product_id
        if not stamp_product_id:
            raise openerp.exceptions.Warning(
                _('Missing tax stamp product in company settings!')
            )
        return stamp_product_id

    def _build_tax_stamp_lines(self, cr, uid, invoice, product, context=None):
        if (
                not product.property_account_income or
                not product.property_account_expense
        ):
            raise openerp.exceptions.Warning(_(
                "Product %s must have income and expense accounts"
            ) % product.name)

        income_vals = {
            'name': _('Tax Stamp Income'),
            'partner_id': invoice.partner_id.id,
            'account_id': product.property_account_income.id,
            'journal_id': invoice.journal_id.id,
            'date': invoice.date_invoice,
            'debit': 0,
            'credit': product.list_price,
        }
        if invoice.type == 'out_refund':
            income_vals['debit'] = product.list_price
            income_vals['credit'] = 0

        expense_vals = {
            'name': _('Tax Stamp Expense'),
            'partner_id': invoice.partner_id.id,
            'account_id': product.property_account_expense.id,
            'journal_id': invoice.journal_id.id,
            'date': invoice.date_invoice,
            'debit': product.list_price,
            'credit': 0,
        }
        if invoice.type == 'out_refund':
            income_vals['debit'] = 0
            income_vals['credit'] = product.list_price

        return income_vals, expense_vals

    _columns = {
        'tax_stamp': fields.function(
            _compute_tax_stamp, type='boolean', string='Tax Stamp'),
    }

    def is_tax_stamp_line_present(self, cr, uid, invoice, context=None):
        for l in invoice.invoice_line:
            if l.is_stamp_line:
                return l.id
        return False

    def is_tax_stamp_applicable(self, cr, uid, invoice, context=None):
        stamp_product_id = invoice.company_id.tax_stamp_product_id
        if not stamp_product_id:
            raise openerp.exceptions.Warning(
                _('Missing tax stamp product in company settings!')
            )
        total_tax_base = 0.0
        invoice_tax_obj = self.pool.get('account.invoice.tax')
        taxes = invoice_tax_obj.compute(cr, uid, invoice.id, context=context)
        tax_base_amounts = {}
        for key in taxes.keys():
            tax_base_amounts[key[1]] = tax_base_amounts.get(
                key[1], 0.0) + taxes[key]['base_amount']
        apply_base_code_ids = [
            t.base_code_id.id for t in stamp_product_id.stamp_apply_tax_ids]
        for tax_code_id in tax_base_amounts.keys():
            if tax_code_id in apply_base_code_ids:
                total_tax_base += tax_base_amounts[tax_code_id]
        if total_tax_base >= stamp_product_id.stamp_apply_min_total_base:
            return True
        else:
            return False

    def add_tax_stamp_line(self, cr, uid, ids, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        for inv in self.browse(cr, uid, ids, context):
            if not inv.tax_stamp:
                raise openerp.exceptions.Warning(
                    _("Tax stamp is not applicable"))
            stamp_product_id = self._get_stamp_product(
                cr, uid, inv, context=context)
            stamp_line_id = self.is_tax_stamp_line_present(
                cr, uid, inv, context=context)
            if stamp_line_id:
                    raise openerp.exceptions.Warning(_(
                        "Tax stamp line %s already present. Remove it first."
                    ) % self.pool.get('account.invoice.line').browse(
                        cr, uid, stamp_line_id, context).name)
            stamp_account = stamp_product_id.property_account_income
            if not stamp_account:
                raise openerp.exceptions.Warning(
                    _('Missing account income configuration for'
                      ' %s') % stamp_product_id.name)
            self.pool.get('account.invoice.line').create(cr, uid, {
                'invoice_id': inv.id,
                'product_id': stamp_product_id.id,
                'name': (stamp_product_id.description_sale or
                         stamp_product_id.name),
                'sequence': 99999,
                'account_id': stamp_account.id,
                'price_unit': stamp_product_id.list_price,
                'quantity': 1,
                'uos_id': stamp_product_id.uom_id.id,
                'invoice_line_tax_id': [
                    (6, 0, [t.id for t in stamp_product_id.taxes_id])],
                'account_analytic_id': None,
            }, context=context)

    def action_move_create(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        line_model = self.pool.get('account.move.line')
        res = super(account_invoice, self).action_move_create(
            cr, uid, ids, context=context)
        for inv in self.browse(cr, uid, ids, context):
            if inv.tax_stamp and not self.is_tax_stamp_line_present(
                    cr, uid, inv, context=context):
                if inv.move_id.state == 'posted':
                    posted = True
                    inv.move_id.state = 'draft'
                stamp_product_id = self._get_stamp_product(
                    cr, uid, inv, context=context)
                income_vals, expense_vals = self._build_tax_stamp_lines(
                    cr, uid, inv, stamp_product_id, context=context)
                income_vals['move_id'] = inv.move_id.id
                expense_vals['move_id'] = inv.move_id.id
                period_id = inv.move_id.period_id.id
                ctx = context.copy()
                ctx.update({
                    'check_move_validity': False,
                    'period_id': period_id,
                })
                line_model.create(cr, uid, income_vals, ctx)
                line_model.create(cr, uid, expense_vals, ctx)
                if posted:
                    inv.move_id.state = 'posted'
        return res


class account_invoice_line(Model):
    _inherit = "account.invoice.line"

    _columns = {
        'is_stamp_line': fields.related(
            'product_id', 'is_stamp', type='boolean',
            relation='product.product', readonly=True, string='Is stamp line'),
    }
