# -*- coding: utf-8 -*-
# Copyright 2017 Nicola Malcontenti - Agile Business Group
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleFiscalCode(WebsiteSale):

    def _get_mandatory_billing_fields(self):
        res = super(
            WebsiteSaleFiscalCode, self
        )._get_mandatory_billing_fields()
        res.append('fiscalcode')
        return res

    def _checkout_form_save(self, mode, checkout, all_values):
        res = super(WebsiteSaleFiscalCode, self)._checkout_form_save(
            mode, checkout, all_values)
        if 'fiscalcode' not in checkout and 'fiscalcode' in all_values:
            request.env['res.partner'].browse(res).sudo().write(
                {'fiscalcode': all_values['fiscalcode']})
        return res
