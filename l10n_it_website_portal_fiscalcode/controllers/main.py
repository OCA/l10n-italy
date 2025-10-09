# Copyright 2019 Simone Rubino
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError, ValidationError
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal


class WebsitePortalFiscalCode(CustomerPortal):
    def _get_optional_fields(self):
        optional_fields = super()._get_optional_fields()
        optional_fields.append("l10n_it_codice_fiscale")
        return optional_fields

    def details_form_validate(self, data, partner_creation=False):
        error, error_message = super().details_form_validate(
            data, partner_creation=partner_creation
        )
        # Check fiscalcode
        partner = request.env.user.partner_id
        # company_type does not come from page form
        company_type = partner.company_type
        company_name = False
        if "company_name" in data:
            company_name = data.get("company_name")
        else:
            # when company_name is not posted (readonly)
            if partner.company_name:
                company_name = partner.company_name
            elif partner.company_type == "company":
                company_name = partner.name
        dummy_partner = request.env["res.partner"].new(
            {
                "l10n_it_codice_fiscale": data.get("l10n_it_codice_fiscale"),
                "company_name": company_name,
                "company_type": company_type,
            }
        )
        try:
            dummy_partner.validate_codice_fiscale()
        except (UserError, ValidationError) as e:
            error["l10n_it_codice_fiscale"] = "error"
            error_message.append(e.args[0])
        return error, error_message
