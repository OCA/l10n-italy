# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.osv import fields, orm


class ResCompany(orm.Model):
    _inherit = 'res.company'

    _columns = {
        'automatic_tax_stamp_on_customer_invoices': fields.boolean('Automatic tax stamp on customer invoices'),
        'automatic_tax_stamp_on_supplier_invoices': fields.boolean('Automatic tax stamp on supplier invoices'),
    }


class AccountConfigSettings(orm.TransientModel):
    _inherit = 'account.config.settings'

    _columns = {
        'automatic_tax_stamp_on_customer_invoices': fields.related(
            'company_id', 'automatic_tax_stamp_on_customer_invoices',
            type='boolean',
            string="Automatic tax stamp on customer invoices",
        ),
        'automatic_tax_stamp_on_supplier_invoices': fields.related(
            'company_id', 'automatic_tax_stamp_on_supplier_invoices',
            type='boolean',
            string="Automatic tax stamp on supplier invoices",
        ),
    }

    def onchange_company_id(self, cr, uid, ids, company_id, context=None):
        res = super(AccountConfigSettings, self).onchange_company_id(
            cr, uid, ids, company_id, context=context)
        if company_id:
            company = self.pool.get('res.company').browse(
                cr, uid, company_id, context=context)
            res['value'].update({
                'automatic_tax_stamp_on_customer_invoices': company.automatic_tax_stamp_on_customer_invoices,
                'automatic_tax_stamp_on_supplier_invoices': company.automatic_tax_stamp_on_supplier_invoices,
            })
        else:
            res['value'].update({
                'automatic_tax_stamp_on_customer_invoices': False,
                'automatic_tax_stamp_on_supplier_invoices': False,
            })
        return res
