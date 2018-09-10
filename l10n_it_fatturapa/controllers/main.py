# -*- coding: utf-8 -*-

from odoo.http import Controller, route, request


class FatturaElettronicaController(Controller):

    #------------------------------------------------------
    # Report controllers
    #------------------------------------------------------
    @route([
        '/fatturapa/preview/<attachment_id>',
    ], type='http', auth='user', website=True)
    def pdf_preview(self, attachment_id, **data):
        attach = request.env['ir.attachment'].browse(int(attachment_id))
        html = attach.get_fattura_elettronica_preview()
        pdf = request.env['report']._run_wkhtmltopdf(
            [], [], [[False, html]], None, None)
        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'), ('Content-Length', len(pdf)),
            # (
            #     'Content-Disposition', 'attachment; '
            #     'filename="fatturaelettronica%s.pdf"' % attachment_id
            # ),
        ]
        return request.make_response(pdf, headers=pdfhttpheaders)
