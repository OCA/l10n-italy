# Copyright 2017 Nicola Malcontenti - Agile Business Group

from odoo.exceptions import ValidationError
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleFiscalCode(WebsiteSale):
    def _checkout_form_save(self, mode, checkout, all_values):
        res = super()._checkout_form_save(mode, checkout, all_values)
        partner_values = dict()
        if "fiscalcode" not in checkout and "fiscalcode" in all_values:
            partner_values["fiscalcode"] = all_values["fiscalcode"]
        if partner_values:
            request.env["res.partner"].browse(res).sudo().write(partner_values)
        return res

    def checkout_form_validate(self, mode, all_form_values, data):
        error, error_message = super().checkout_form_validate(
            mode, all_form_values, data
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
                "fiscalcode": data.get("fiscalcode"),
                "company_name": company_name,
                "company_type": company_type,
            }
        )
        try:
            dummy_partner.check_fiscalcode()
        except ValidationError as e:
            error["fiscalcode"] = "error"
            error_message.append(e)
        return error, error_message
