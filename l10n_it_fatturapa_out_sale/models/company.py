# -*- coding: utf-8 -*-
# Copyright 2019 Sergio Corato <https://github.com/sergiocorato>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    fatturapa_out_sale_internal_ref = fields.Boolean(
        string="Internal sale order reference",
        help="Put in e-invoice reference to internal order, instead of "
             "reference of customer.")
    fatturapa_sale_order_data = fields.Boolean(
        string='Include sale order data in e-invoice')


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    fatturapa_out_sale_internal_ref = fields.Boolean(
        related='company_id.fatturapa_out_sale_internal_ref',
        string="Internal sale order reference",
        help="Put in e-invoice reference to internal order, instead of "
             "reference of customer.")
    fatturapa_sale_order_data = fields.Boolean(
        related='company_id.fatturapa_sale_order_data',
        string='Include sale order data in e-invoice')

    @api.onchange('company_id')
    def onchange_company_id(self):
        res = super(AccountConfigSettings, self).onchange_company_id()
        if self.company_id:
            company = self.company_id
            self.fatturapa_out_sale_internal_ref = (
                company.fatturapa_out_sale_internal_ref)
            self.fatturapa_sale_order_data = (
                company.fatturapa_sale_order_data)
        else:
            self.fatturapa_out_sale_internal_ref = False
            self.fatturapa_sale_order_data = False
        return res
