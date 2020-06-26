# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    asset_accounting_info_ids = fields.One2many(
        'asset.accounting.info',
        'invoice_line_id',
        string="Assets Accounting Info"
    )

    asset_ids = fields.Many2many(
        'asset.asset',
        compute='_compute_asset_data',
        store=True,
        string="Assets"
    )

    dep_line_ids = fields.Many2many(
        'asset.depreciation.line',
        compute='_compute_asset_data',
        store=True,
        string="Depreciation Lines"
    )

    @api.constrains('company_id')
    def check_company(self):
        for inv_line in self:
            comp = inv_line.get_linked_aa_info_records().mapped('company_id')
            if len(comp) > 1 or (comp and comp != inv_line.company_id):
                raise ValidationError(
                    _("`{}`: cannot change invoice line's company once it's"
                      " already related to an asset.")
                    .format(inv_line.name_get()[0][-1])
                )

    @api.multi
    @api.depends('asset_accounting_info_ids',
                 'asset_accounting_info_ids.asset_id',
                 'asset_accounting_info_ids.dep_line_id')
    def _compute_asset_data(self):
        for line in self:
            aa_info = line.get_linked_aa_info_records()
            assets = aa_info.mapped('asset_id')
            dep_lines = aa_info.mapped('dep_line_id')
            if dep_lines:
                assets += dep_lines.mapped('asset_id')
            line.update({
                'asset_ids': [(6, 0, assets.ids)],
                'dep_line_ids': [(6, 0, dep_lines.ids)],
            })

    def get_asset_purchase_amount(self, currency=None):
        purchase_amount = 0

        for line in self:
            # Standard line amount
            purchase_amount += line.currency_id.compute(
                line.price_subtotal, currency
            )
            if line.invoice_line_tax_ids:
                # Get taxes
                discount = line.price_unit * (line.discount or 0.0) / 100
                price_unit = line.price_unit - discount
                line_currency = line.currency_id
                qty = line.quantity
                product = line.product_id
                partner = line.invoice_id.partner_id
                taxes = line.invoice_line_tax_ids.compute_all(
                    price_unit, line_currency, qty, product, partner
                ).get('taxes') or []
                # Add non-deductible taxes
                for tax_dict in taxes:
                    if not (tax_dict.get('account_id')
                            or tax_dict.get('refund_account_id')) \
                            and tax_dict.get('amount'):
                        purchase_amount += line.currency_id.compute(
                            tax_dict.get('amount'), currency
                        )

        return purchase_amount

    def get_linked_aa_info_records(self):
        self.ensure_one()
        return self.asset_accounting_info_ids
