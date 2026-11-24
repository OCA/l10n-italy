# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from io import BytesIO

from lxml import etree

from odoo import tools
from odoo.exceptions import UserError
from odoo.http import Controller, request, route

_logger = logging.getLogger(__name__)


class FatturaPAController(Controller):
    def get_fatturapa_preview_style_name(self):
        """Hook to have a clean inheritance."""
        return "FoglioStileAssoSoftware.xsl"

    def get_xml_string(self, doc_data):
        name = doc_data.get("filename", "")
        content = doc_data.get("content", b"")
        xml_tree = request.env["account.move"]._parse_xml_with_recovery(
            content, name=name
        )
        if xml_tree is None:
            _logger.info("Italian EDI invoice file %s cannot be decoded.", name)
            raise UserError(request.env._("The e-invoice %s cannot be decoded.", name))

        xml_string = etree.tostring(
            xml_tree, pretty_print=True, encoding="unicode"
        ).encode()
        return xml_string

    def get_fattura_elettronica_preview(self, doc_data):
        xsl_path = tools.misc.file_path(
            f"l10n_it_edi_extension/data/{self.get_fatturapa_preview_style_name()}"
        )
        xslt = etree.parse(xsl_path)

        xml_string = self.get_xml_string(doc_data)
        xml_file = BytesIO(xml_string)
        recovering_parser = etree.XMLParser(recover=True, resolve_entities=False)
        dom = etree.parse(xml_file, parser=recovering_parser)
        transform = etree.XSLT(xslt)
        newdom = transform(dom)
        return etree.tostring(newdom, pretty_print=True, encoding="unicode")

    @route(
        [
            "/fatturapa/preview/<int:invoice_id>",
            "/fatturapa/preview/<int:invoice_id>/<string:filetype>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def fatturapa_preview(self, invoice_id, filetype="fatturapa", **data):
        # "fatturapa" is the e-invoice sent to the SdI,
        # "fatturapa_in" is the imported e-invoice
        if filetype not in ("fatturapa", "fatturapa_in"):
            raise request.not_found()
        invoice = request.env["account.move"].browse(invoice_id).exists()
        if not invoice:
            raise request.not_found()
        invoice.check_access("read")

        doc_data = invoice.sudo()._get_invoice_legal_documents(filetype)
        if not doc_data:
            raise request.not_found()

        html = self.get_fattura_elettronica_preview(doc_data)
        if isinstance(html, bytes):
            html = html.decode()
        pdf = request.env["ir.actions.report"]._run_wkhtmltopdf([html])

        pdfhttpheaders = [
            ("Content-Type", "application/pdf"),
            ("Content-Length", len(pdf)),
        ]
        return request.make_response(pdf, headers=pdfhttpheaders)
