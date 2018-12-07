# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import fields, api, models, exceptions
from openerp.tools.translate import _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def compute_stamps(self):
        invoice_line_obj = self.env['account.invoice.line']
        invoice_tax_obj = self.env['account.invoice.tax']
        for inv in self:
            stamp_product_id = self.env.user.with_context(
                    lang=inv.partner_id.lang).company_id.tax_stamp_product_id
            if not stamp_product_id:
                raise exceptions.Warning(
                    _('Missing tax stamp product in company settings!')
                )
            for l in inv.invoice_line:
                if l.product_id and l.product_id.is_stamp:
                    l.unlink()
            taxes = invoice_tax_obj.compute(inv)
            tax_base_amounts = {}
            for key in taxes.keys():
                tax_base_amounts[key[1]] = tax_base_amounts.get(
                    key[1], 0.0) + taxes[key]['base_amount']
            total_tax_base = 0.0
            for tax_code_id in tax_base_amounts.keys():
                if tax_code_id in stamp_product_id.stamp_apply_tax_ids.mapped(
                        'base_code_id.id'):
                    total_tax_base += tax_base_amounts[tax_code_id]
            taxes = stamp_product_id.taxes_id
            if inv.type in ('in_invoice', 'in_refund'):
                total_tax_base = total_tax_base * -1.0
                taxes = stamp_product_id.supplier_taxes_id
            if inv.fiscal_position:
                taxes_ids = inv.fiscal_position.map_tax(taxes)
            else:
                taxes_ids = taxes

            if total_tax_base >= stamp_product_id.stamp_apply_min_total_base:
                if inv.type in ('out_invoice', 'out_refund'):
                    stamp_account = stamp_product_id.property_account_income
                else:
                    stamp_account = stamp_product_id.property_account_expense
                if not stamp_account:
                    raise exceptions.Warning(
                        _('Missing account income/expense configuration for'
                          ' %s') % stamp_product_id.name)
                invoice_line_obj.create({
                        'invoice_id': inv.id,
                        'product_id': stamp_product_id.id,
                        'name': stamp_product_id.description_sale,
                        'sequence': 99999,
                        'account_id': stamp_account.id,
                        'price_unit': stamp_product_id.list_price,
                        'quantity': 1,
                        'uos_id': stamp_product_id.uom_id.id,
                        'invoice_line_tax_id': [
                            (6, 0, taxes_ids.ids)],
                        'account_analytic_id': None,
                    })

    @api.multi
    def button_reset_taxes(self):
        self.compute_stamps()
        return super(AccountInvoice, self).button_reset_taxes()

    @api.multi
    def action_move_create(self):
        self.compute_stamps()
        return super(AccountInvoice,self).action_move_create()


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    is_stamp_line = fields.Boolean(
        related='product_id.is_stamp',
        readonly=True)
