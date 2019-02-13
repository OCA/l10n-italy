# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.osv import fields, orm


class ResCompany(orm.Model):
    _inherit = 'res.company'

    _columns = {
        'tax_stamp_product_id': fields.many2one(
            'product.product', 'Tax Stamp Product',
            help="Product used to model DatiBollo XML element on bills."
        )
    }


class AccountConfigSettings(orm.TransientModel):
    _inherit = 'account.config.settings'

    _columns = {
        'tax_stamp_product_id': fields.related(
            'company_id', 'tax_stamp_product_id',
            type='many2one', relation='product.product',
            string="Tax Stamp Product",
            help="Product used to model DatiBollo XML element on bills."
        )
    }

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
