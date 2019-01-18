# -*- coding: utf-8 -*-
# Copyright 2019 Simone Rubino
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _
from odoo.addons.website_portal.controllers.main import website_account
from odoo.http import request

website_account.OPTIONAL_BILLING_FIELDS.extend(
    ['fiscalcode', 'individual', 'is_company'])


class WebsitePortalFiscalCode(website_account):

    def details_form_validate(self, data):
        error, error_message = \
            super(WebsitePortalFiscalCode, self).details_form_validate(data)
        data['individual'] = not data.get('is_company')
        dummy_partner = request.env['res.partner'].new({
            'fiscalcode': data.get('fiscalcode'),
            'individual': data.get('individual')
        })
        if not dummy_partner.check_fiscalcode():
            error['fiscalcode'] = 'error'
            error['is_company'] = 'error'
            error_message.append(_('Fiscal Code not valid'))
        return error, error_message
