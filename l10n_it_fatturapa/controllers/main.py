from odoo.http import Controller, request, route


class FatturaElettronicaController(Controller):
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
        html = attach.get_fattura_elettronica_preview()
        return request.make_response(html)
