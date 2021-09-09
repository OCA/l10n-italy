# Copyright 2019 Simone Rubino
# Copyright 2019 Lorenzo Battistini
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.exceptions import ValidationError
from odoo.http import request
from odoo.addons.l10n_it_website_portal_fiscalcode.controllers.main import \
    WebsitePortalFiscalCode
from odoo.tools.translate import _

FATTURAPA_PORTAL_FIELDS = \
    ['codice_destinatario', 'firstname', 'lastname',
     'pec_destinatario', 'country_id', 'fiscalcode', 'zipcode', 'vat',
     'electronic_invoice_subjected', 'street', 'city',
     'is_pa', 'ipa_code', 'eori_code', 'electronic_invoice_obliged_subject']
WebsitePortalFiscalCode.OPTIONAL_BILLING_FIELDS.extend(FATTURAPA_PORTAL_FIELDS)


class WebsitePortalFatturapa(WebsitePortalFiscalCode):

    def details_form_validate(self, data):
        # when checkbox electronic_invoice_subjected is not checked,
        # it is not posted
        data['electronic_invoice_subjected'] = data.get(
            'electronic_invoice_subjected', False)
        if data["electronic_invoice_subjected"]:
            data["electronic_invoice_obliged_subject"] = True
        error, error_message = \
            super(WebsitePortalFatturapa, self).details_form_validate(data)
        partner_sudo = request.env.user.partner_id.sudo()
        error, error_message = \
            self.validate_partner_firstname(data, error, error_message)

        partner_values = self.get_portal_fatturapa_partner_values(
            data, partner_sudo)
        dummy_partner = request.env['res.partner'].new(partner_values)
        try:
            dummy_partner._check_ftpa_partner_data()
        except ValidationError as ve:
            error['error'] = 'error'
            error_message.append(ve.name)
        return error, error_message

    def get_portal_fatturapa_partner_values(self, data, partner_sudo):
        # Read all the fields for the constraint from the current user
        constr_fields = partner_sudo._check_ftpa_partner_data._constrains
        partner_values = partner_sudo.read(constr_fields)[0]

        # Update them with fields that might be edited by the user
        new_partner_values = {f_name: data.get(f_name)
                              for f_name in FATTURAPA_PORTAL_FIELDS}
        if new_partner_values.get('country_id'):
            new_partner_values['country_id'] = \
                int(new_partner_values['country_id'])
        new_partner_values.update({
            'zip': new_partner_values.pop('zipcode', '')})
        partner_values.update(new_partner_values)
        return partner_values

    def validate_partner_firstname(self, data, error, error_message):
        # Compute name field, using First name and Last name
        if all(f in data for f in ['name', 'firstname', 'lastname']):
            lastname = data.get('lastname')
            firstname = data.get('firstname')
            if lastname or firstname:
                data.update(
                    name=request.env['res.partner']._get_computed_name(
                        lastname, firstname))
            else:
                error['firstname'] = 'error'
                error['lastname'] = 'error'
                error_message.append(
                    _('At least one of first name and last name is required'))
        return error, error_message
