# -*- coding: utf-8 -*-
# Copyright 2019 Simone Rubino
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _
from odoo.addons.website_portal.controllers.main import website_account
from odoo.http import request

website_account.OPTIONAL_BILLING_FIELDS.extend(['fiscalcode'])


class WebsitePortalFiscalCode(website_account):

    def details_form_validate(self, data):
        error, error_message = \
            super(WebsitePortalFiscalCode, self).details_form_validate(data)
        # Check fiscalcode
        partner_sudo = request.env.user.partner_id.sudo()
        dummy_partner = request.env['res.partner'].new({
            'fiscalcode': data.get('fiscalcode'),
            'individual': partner_sudo.individual
        })
        if not dummy_partner.check_fiscalcode():
            error['fiscalcode'] = 'error'
            error_message.append(_('Fiscal Code not valid'))
        return error, error_message
