from odoo.http import Controller, route, request


class FatturaElettronicaController(Controller):

    @route([
        '/fatturapa/preview/<attachment_id>',
    ], type='http', auth='user', website=True)
    def pdf_preview(self, attachment_id, **data):
        attach = request.env['ir.attachment'].browse(int(attachment_id))
        fatturapa_attachment_model = request.env['fatturapa.attachment']
        html = fatturapa_attachment_model \
            .get_fattura_elettronica_preview(attach)
        pdf = request.env['ir.actions.report']._run_wkhtmltopdf(
            [html])

        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'), ('Content-Length', len(pdf)
                                                  )]
        return request.make_response(pdf, headers=pdfhttpheaders)
