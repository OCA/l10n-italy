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
        fatturapa_attachment_model = request.env["fatturapa.attachment"]
        html = fatturapa_attachment_model.get_fattura_elettronica_preview(attach)
        return request.make_response(html)
