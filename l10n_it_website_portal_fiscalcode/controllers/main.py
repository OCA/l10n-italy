# Copyright 2019 Simone Rubino
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _
from odoo.exceptions import ValidationError
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal

CustomerPortal.OPTIONAL_BILLING_FIELDS.extend(["fiscalcode"])


class WebsitePortalFiscalCode(CustomerPortal):
    def details_form_validate(self, data):
        error, error_message = super(
            WebsitePortalFiscalCode, self
        ).details_form_validate(data)
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
                "fiscalcode": data.get("fiscalcode"),
                "company_name": company_name,
                "company_type": company_type,
            }
        )
        try:
            dummy_partner.check_fiscalcode()
        except ValidationError:
            error["fiscalcode"] = "error"
            error_message.append(_("Fiscal Code not valid"))
        return error, error_message
