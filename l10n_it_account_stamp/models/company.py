# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    account_stamp_product_id = fields.Many2one(
        'product.product', 'Stamp Data Product',
        help="Product used to model DatiBollo XML element on bills."
        )


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    account_stamp_product_id = fields.Many2one(
        related='company_id.account_stamp_product_id',
        string="Stamp Data Product",
        help="Product used to model DatiBollo XML element on bills."
        )

    @api.v7
    def onchange_company_id(self, cr, uid, ids, company_id, context=None):
        res = super(AccountConfigSettings, self).onchange_company_id(
            cr, uid, ids, company_id, context=context)
        if company_id:
            company = self.pool.get('res.company').browse(
                cr, uid, company_id, context=context)
            res['value'].update({
                'account_stamp_product_id': (
                    company.account_stamp_product_id and
                    company.account_stamp_product_id.id or False
                    )
            })
        else:
            res['value'].update({
                'account_stamp_product_id': False})
        return res
