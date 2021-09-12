from odoo.addons.portal.controllers.portal import CustomerPortal

CustomerPortal.OPTIONAL_BILLING_FIELDS.extend(["use_corrispettivi", "use_invoices"])


class WebsitePortalCorrispettivi(CustomerPortal):

    def details_form_validate(self, data):
        if data.get("use_invoices", False):
            data["use_corrispettivi"] = False
        else:
            data["use_corrispettivi"] = True
        return super(WebsitePortalCorrispettivi, self).details_form_validate(data)
