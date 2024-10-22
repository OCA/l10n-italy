from odoo.http import Controller, request, route


class FatturaElettronicaController(Controller):
    def _get_allowed_company_ids(self):
        """Return list of allowed companies for request.

        Default to the user's default company.
        """
        # The allowed companies are set in the cookies in JS,
        # specifically in https://github.com/odoo/odoo/
        #   blob/441c94270a4935d2b0b67a9f8201fcba9d15d957/
        #   addons/web/static/src/legacy/js/core/session.js#L338
        allowed_company_ids_string = request.httprequest.cookies.get("cids")
        if allowed_company_ids_string is not None:
            allowed_company_ids = [
                int(allowed_company_id_string)
                for allowed_company_id_string in allowed_company_ids_string.split(",")
            ]
        else:
            allowed_company_ids = [
                request.env.user.company_id.id,
            ]
        return allowed_company_ids

    @route(
        [
            "/fatturapa/preview/<attachment_id>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def pdf_preview(self, attachment_id, **data):
        attach = request.env["ir.attachment"].browse(int(attachment_id))
        fatturapa_attachment_model = request.env["fatturapa.attachment"]
        allowed_company_ids = self._get_allowed_company_ids()
        html = fatturapa_attachment_model.with_context(
            allowed_company_ids=allowed_company_ids,
        ).get_fattura_elettronica_preview(attach)
        return request.make_response(html)
