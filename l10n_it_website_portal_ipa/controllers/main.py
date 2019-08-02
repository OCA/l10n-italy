#  Copyright 2019 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.portal.controllers.portal import CustomerPortal


class IPACustomerPortal(CustomerPortal):
    CustomerPortal.OPTIONAL_BILLING_FIELDS.extend(['is_pa', 'ipa_code'])

    def details_form_validate(self, data):
        # False Checkboxes are not posted in HTML forms
        if 'is_pa' not in data:
            data['is_pa'] = False
        return super().details_form_validate(data)
