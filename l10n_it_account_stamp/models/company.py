# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from openerp import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    tax_stamp_product_id = fields.Many2one(
        'product.product', 'Tax Stamp Product',
        help="Product used as Tax Stamp in customer invoices."
        )


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    tax_stamp_product_id = fields.Many2one(
        related='company_id.tax_stamp_product_id',
        string="Tax Stamp Product",
        help="Product used as Tax Stamp in customer invoices."
        )

    @api.v7
    def onchange_company_id(self, cr, uid, ids, company_id, context=None):
        res = super(AccountConfigSettings, self).onchange_company_id(
            cr, uid, ids, company_id, context=context)
        if company_id:
            company = self.pool.get('res.company').browse(
                cr, uid, company_id, context=context)
            res['value'].update({
                'tax_stamp_product_id': (
                    company.tax_stamp_product_id and
                    company.tax_stamp_product_id.id or False
                    )
            })
        else:
            res['value'].update({
                'tax_stamp_product_id': False})
        return res
