# -*- coding: utf-8 -*-

from openerp.http import Controller, route, request


class FatturaElettronicaController(Controller):

    @route([
        '/fatturapa/preview/<attachment_id>',
    ], type='http', auth='user', website=True)
    def pdf_preview(self, attachment_id, **data):
        attach = request.env['ir.attachment'].browse(int(attachment_id))
        html = attach.get_fattura_elettronica_preview()
        pdf = request.env['report']._run_wkhtmltopdf(
            [], [], [[False, html]], None, None)
        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))
        ]
        return request.make_response(pdf, headers=pdfhttpheaders)
