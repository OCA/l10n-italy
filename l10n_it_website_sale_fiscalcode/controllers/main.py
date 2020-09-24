# Copyright 2017 Nicola Malcontenti - Agile Business Group

from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import _


class WebsiteSaleFiscalCode(WebsiteSale):

    def _checkout_form_save(self, mode, checkout, all_values):
        res = super(WebsiteSaleFiscalCode, self)._checkout_form_save(
            mode, checkout, all_values)
        partner_values = dict()
        if 'fiscalcode' not in checkout and 'fiscalcode' in all_values:
            partner_values['fiscalcode'] = all_values['fiscalcode']
        if partner_values:
            request.env['res.partner'].browse(res).sudo().write(partner_values)
        return res

    def checkout_form_validate(self, mode, all_form_values, data):
        error, error_message = super().checkout_form_validate(
            mode, all_form_values, data)
        partner_sudo = request.env.user.partner_id.sudo()
        dummy_partner = request.env['res.partner'].new({
            'fiscalcode': data.get('fiscalcode'),
            'is_company': partner_sudo.is_company
        })
        if not dummy_partner.check_fiscalcode():
            error['fiscalcode'] = 'error'
            error_message.append(_('Fiscal Code not valid'))
        return error, error_message
