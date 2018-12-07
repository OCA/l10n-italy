# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from openerp import fields, api, models, exceptions
from openerp.tools.translate import _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    tax_stamp = fields.Boolean(
        "Tax Stamp", readonly=True, states={'draft': [('readonly', False)]},
        compute='_compute_tax_stamp')

    def is_tax_stamp_applicable(self):
        stamp_product_id = self.env.user.with_context(
            lang=self.partner_id.lang).company_id.tax_stamp_product_id
        if not stamp_product_id:
            raise exceptions.Warning(
                _('Missing tax stamp product in company settings!')
            )
        total_tax_base = 0.0
        taxes = self.env['account.invoice.tax'].compute(self)
        tax_base_amounts = {}
        for key in taxes.keys():
            tax_base_amounts[key[1]] = tax_base_amounts.get(
                key[1], 0.0) + taxes[key]['base_amount']
        for tax_code_id in tax_base_amounts.keys():
            if tax_code_id in stamp_product_id.stamp_apply_tax_ids.mapped(
                    'base_code_id.id'):
                total_tax_base += tax_base_amounts[tax_code_id]
        if total_tax_base >= stamp_product_id.stamp_apply_min_total_base:
            return True
        else:
            return False

    @api.one
    @api.depends('tax_line')
    def _compute_tax_stamp(self):
        if self.is_tax_stamp_applicable():
            self.tax_stamp = True
        else:
            self.tax_stamp = False

    def _get_stamp_product(self, inv):
        stamp_product_id = self.env.user.with_context(
            lang=inv.partner_id.lang).company_id.tax_stamp_product_id
        if not stamp_product_id:
            raise exceptions.Warning(
                _('Missing tax stamp product in company settings!')
            )
        return stamp_product_id

    @api.multi
    def add_tax_stamp_line(self):
        for inv in self:
            if not inv.tax_stamp:
                raise exceptions.Warning(_("Tax stamp is not applicable"))
            stamp_product_id = self._get_stamp_product(inv)
            for l in inv.invoice_line:
                if l.product_id and l.product_id.is_stamp:
                    raise exceptions.Warning(_(
                        "Tax stamp line %s already present. Remove it first."
                    ) % l.name)
            stamp_account = stamp_product_id.property_account_income
            if not stamp_account:
                raise exceptions.Warning(
                    _('Missing account income configuration for'
                      ' %s') % stamp_product_id.name)
            self.env['account.invoice.line'].create({
                'invoice_id': inv.id,
                'product_id': stamp_product_id.id,
                'name': stamp_product_id.description_sale or
                stamp_product_id.name,
                'sequence': 99999,
                'account_id': stamp_account.id,
                'price_unit': stamp_product_id.list_price,
                'quantity': 1,
                'uos_id': stamp_product_id.uom_id.id,
                'invoice_line_tax_id': [
                    (6, 0, stamp_product_id.taxes_id.ids)],
                'account_analytic_id': None,
            })

    def is_tax_stamp_line_present(self):
        for l in self.invoice_line:
            if l.is_stamp_line:
                return True
        return False

    def _build_tax_stamp_lines(self, product):
        if (
            not product.property_account_income or
            not product.property_account_expense
        ):
            raise exceptions.Warning(_(
                "Product %s must have income and expense accounts"
            ) % product.name)

        income_vals = {
            'name': _('Tax Stamp Income'),
            'partner_id': self.partner_id.id,
            'account_id': product.property_account_income.id,
            'journal_id': self.journal_id.id,
            'date': self.date_invoice,
            'debit': 0,
            'credit': product.list_price,
            }
        if self.type == 'out_refund':
            income_vals['debit'] = product.list_price
            income_vals['credit'] = 0

        expense_vals = {
            'name': _('Tax Stamp Expense'),
            'partner_id': self.partner_id.id,
            'account_id': product.property_account_expense.id,
            'journal_id': self.journal_id.id,
            'date': self.date_invoice,
            'debit': product.list_price,
            'credit': 0,
            }
        if self.type == 'out_refund':
            income_vals['debit'] = 0
            income_vals['credit'] = product.list_price

        return income_vals, expense_vals

    @api.multi
    def action_move_create(self):
        res = super(AccountInvoice, self).action_move_create()
        for inv in self:
            if inv.tax_stamp and not inv.is_tax_stamp_line_present():
                if inv.move_id.state == 'posted':
                    posted = True
                    inv.move_id.state = 'draft'
                line_model = self.env['account.move.line']
                stamp_product_id = self._get_stamp_product(inv)
                income_vals, expense_vals = self._build_tax_stamp_lines(
                    stamp_product_id)
                income_vals['move_id'] = inv.move_id.id
                expense_vals['move_id'] = inv.move_id.id
                period_id = inv.move_id.period_id.id
                line_model.with_context(
                    check_move_validity=False,
                    period_id=period_id,
                ).create(income_vals)
                line_model.with_context(
                    check_move_validity=False,
                    period_id=period_id,
                ).create(expense_vals)
                if posted:
                    inv.move_id.state = 'posted'
        return res


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    is_stamp_line = fields.Boolean(
        related='product_id.is_stamp',
        readonly=True)
