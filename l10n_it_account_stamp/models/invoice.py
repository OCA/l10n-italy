# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, api, models, exceptions, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def compute_stamps(self):
        invoice_line_obj = self.env['account.invoice.line']
        for inv in self:
            if inv.type in ('in_invoice', 'in_refund'):
                continue
            stamp_product_id = self.env.user.with_context(
                lang=inv.partner_id.lang).company_id.tax_stamp_product_id
            if not stamp_product_id:
                raise exceptions.Warning(
                    _('Missing tax stamp product in company settings!')
                )
            for l in inv.invoice_line_ids:
                if l.product_id and l.product_id.is_stamp:
                    l.unlink()
            total_tax_base = 0.0
            for inv_tax in inv.tax_line_ids:
                if (
                    inv_tax.tax_id.id in
                    stamp_product_id.stamp_apply_tax_ids.ids
                ):
                    total_tax_base += inv_tax.base
            taxes_ids = stamp_product_id.taxes_id

            if total_tax_base >= stamp_product_id.stamp_apply_min_total_base:
                stamp_account = stamp_product_id.property_account_income_id
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
                        'uom_id': stamp_product_id.uom_id.id,
                        'invoice_line_tax_ids': [
                            (6, 0, taxes_ids.ids)],
                        'account_analytic_id': None,
                    })

    @api.multi
    def action_move_create(self):
        self.compute_stamps()
        return super(AccountInvoice,self).action_move_create()


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    is_stamp_line = fields.Boolean(
        related='product_id.is_stamp',
        readonly=True)
