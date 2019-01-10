# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, api, models, exceptions, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    tax_stamp = fields.Boolean(
        "Tax Stamp", readonly=True, states={'draft': [('readonly', False)]})

    def is_tax_stamp_applicable(self):
        stamp_product_id = self.env.user.with_context(
            lang=self.partner_id.lang).company_id.tax_stamp_product_id
        if not stamp_product_id:
            raise exceptions.Warning(
                _('Missing tax stamp product in company settings!')
            )
        total_tax_base = 0.0
        for inv_tax in self.tax_line_ids:
            if (
                inv_tax.tax_id.id in
                stamp_product_id.stamp_apply_tax_ids.ids
            ):
                total_tax_base += inv_tax.base
        if total_tax_base >= stamp_product_id.stamp_apply_min_total_base:
            return True
        else:
            return False

    @api.onchange('tax_line_ids')
    def _onchange_tax_line_ids(self):
        if self.is_tax_stamp_applicable():
            self.tax_stamp = True
        else:
            self.tax_stamp = False

    @api.multi
    def add_tax_stamp_line(self):
        for inv in self:
            if not inv.tax_stamp:
                raise exceptions.Warning(_("Tax stamp is not applicable"))
            stamp_product_id = self.env.user.with_context(
                lang=inv.partner_id.lang).company_id.tax_stamp_product_id
            if not stamp_product_id:
                raise exceptions.Warning(
                    _('Missing tax stamp product in company settings!')
                )
            for l in inv.invoice_line_ids:
                if l.product_id and l.product_id.is_stamp:
                    raise exceptions.Warning(_(
                        "Tax stamp line %s already present. Remove it first."
                    ) % l.name)
            stamp_account = stamp_product_id.property_account_income_id
            if not stamp_account:
                raise exceptions.Warning(
                    _('Missing account income configuration for'
                      ' %s') % stamp_product_id.name)
            self.env['account.invoice.line'].create({
                'invoice_id': inv.id,
                'product_id': stamp_product_id.id,
                'name': stamp_product_id.description_sale,
                'sequence': 99999,
                'account_id': stamp_account.id,
                'price_unit': stamp_product_id.list_price,
                'quantity': 1,
                'uom_id': stamp_product_id.uom_id.id,
                'invoice_line_tax_ids': [
                    (6, 0, stamp_product_id.taxes_id.ids)],
                'account_analytic_id': None,
            })
            inv.compute_taxes()

    def is_tax_stamp_line_present(self):
        for l in self.invoice_line_ids:
            if l.product_id and l.product_id.is_stamp:
                return True
        return False

    def _build_tax_stamp_lines(self, product):
        if (
            not product.property_account_income_id or
            not product.property_account_expense_id
        ):
            raise exceptions.Warning(_(
                "Product %s must have income and expense accounts"
            ) % product.name)

        income_vals = {
            'name': _('Tax Stamp Income'),
            'partner_id': self.partner_id.id,
            'account_id': product.property_account_income_id.id,
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
            'account_id': product.property_account_expense_id.id,
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
                stamp_product_id = self.env.user.with_context(
                    lang=inv.partner_id.lang).company_id.tax_stamp_product_id
                if not stamp_product_id:
                    raise exceptions.Warning(
                        _('Missing tax stamp product in company settings!')
                    )
                income_vals, expense_vals = self._build_tax_stamp_lines(
                    stamp_product_id)
                income_vals['move_id'] = inv.move_id.id
                expense_vals['move_id'] = inv.move_id.id
                line_model.with_context(
                    check_move_validity=False
                ).create(income_vals)
                line_model.with_context(
                    check_move_validity=False
                ).create(expense_vals)
                if posted:
                    inv.move_id.state = 'posted'
        return res


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    is_stamp_line = fields.Boolean(
        related='product_id.is_stamp',
        readonly=True)
