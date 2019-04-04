# Copyright 2019 Simone Rubino
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request

CustomerPortal.OPTIONAL_BILLING_FIELDS.extend(['fiscalcode'])


class WebsitePortalFiscalCode(CustomerPortal):

    def details_form_validate(self, data):
        error, error_message = \
            super(WebsitePortalFiscalCode, self).details_form_validate(data)
        # Check fiscalcode
        dummy_partner = request.env['res.partner'].new({
            'fiscalcode': data.get('fiscalcode'),
            'company_name': data.get('company_name'),
        })
        if not dummy_partner.check_fiscalcode():
            error['fiscalcode'] = 'error'
            error_message.append(_('Fiscal Code not valid'))
        return error, error_message
