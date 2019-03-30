# Copyright 2019 Simone Rubino
# Copyright 2019 Lorenzo Battistini
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.exceptions import ValidationError
from odoo.http import request


class WebsiteSaleFatturapa(WebsiteSale):

    def _get_fatturapa_fields(self):
        """Fields that can be changed by the user in frontend"""
        return ['firstname', 'lastname', 'codice_destinatario',
                'pec_destinatario', 'electronic_invoice_subjected',
                'fiscalcode', 'vat', 'street', 'zip', 'city', 'country_id']

    def values_preprocess(self, order, mode, values):
        pre_values = super().values_preprocess(order, mode, values)
        # Compute name field, using First name and Last name
        if all(f in values for f in ['name', 'firstname', 'lastname']):
            partner_model = request.env['res.partner']
            pre_values.update(
                name=partner_model._get_computed_name(
                    pre_values['lastname'],
                    pre_values['firstname']))
        return pre_values

    def checkout_form_validate(self, mode, all_form_values, data):
        error, error_message = super().checkout_form_validate(
            mode, all_form_values, data)

        # when checkbox electronic_invoice_subjected is not checked,
        # it is not posted
        data['electronic_invoice_subjected'] = data.get(
            'electronic_invoice_subjected', False)
        partner_model = request.env['res.partner']
        # Gather the value of each field that needs to be
        # checked for fatturapa constraint from the current partner
        partner_sudo = request.env.user.partner_id.sudo()
        check_fatturapa_fields = \
            partner_model._check_ftpa_partner_data._constrains
        partner_values = partner_sudo.read(check_fatturapa_fields)[0]

        # Update values of the current partner with values changed by the user
        partner_values.update({
            fatt_field: data.get(fatt_field)
            for fatt_field in self._get_fatturapa_fields()
            if fatt_field in data})
        # Patch the country field as it is a m2o so it needs an int
        if partner_values.get('country_id'):
            partner_values['country_id'] = int(partner_values['country_id'])
        # This will be set later, during post_process
        partner_values['customer'] = True

        partner_dummy = partner_model.new(partner_values)
        try:
            partner_dummy._check_ftpa_partner_data()
        except ValidationError as ve:
            error['fatturapa'] = 'error'
            error_message.append(ve.name)
        return error, error_message

    def _checkout_form_save(self, mode, checkout, all_values):
        for fatturapa_field in self._get_fatturapa_fields():
            if fatturapa_field not in checkout \
                    and fatturapa_field in all_values:
                checkout[fatturapa_field] = all_values[fatturapa_field]
        return super()._checkout_form_save(mode, checkout, all_values)
