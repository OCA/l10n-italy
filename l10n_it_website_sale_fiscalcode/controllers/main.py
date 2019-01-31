# -*- coding: utf-8 -*-
# Copyright 2017 Nicola Malcontenti - Agile Business Group
# Copyright 2019 Simone Rubino
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleFiscalCode(WebsiteSale):

    def _checkout_form_save(self, mode, checkout, all_values):
        res = super(WebsiteSaleFiscalCode, self)._checkout_form_save(
            mode, checkout, all_values)
        partner_values = dict()
        # checkout contains some fields of the form
        # (see WebsiteSale.values_postprocess).
        # all_values instead contains all the values of the form.
        # The fields in checkout have already been written in the partner
        # by the super() call then we don't need to write them again.
        if 'fiscalcode' not in checkout and 'fiscalcode' in all_values:
            partner_values['fiscalcode'] = all_values['fiscalcode']
        if 'is_company' not in checkout and 'is_company' in all_values:
            partner_values['is_company'] = all_values['is_company']
            partner_values['individual'] = not all_values['is_company']
        if partner_values:
            request.env['res.partner'].browse(res).sudo().write(partner_values)
        return res

    def checkout_form_validate(self, mode, all_form_values, data):
        error, error_message = super(WebsiteSaleFiscalCode, self) \
            .checkout_form_validate(mode, all_form_values, data)
        data['individual'] = not data.get('is_company')
        dummy_partner = request.env['res.partner'].new({
            'fiscalcode': data.get('fiscalcode'),
            'individual': data.get('individual'),
            'is_company': data.get('is_company')
        })
        if not dummy_partner.check_fiscalcode():
            error['fiscalcode'] = 'error'
            error['is_company'] = 'error'
            error_message.append(_('Fiscal Code not valid'))
        return error, error_message
