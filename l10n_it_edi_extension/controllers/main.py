# Copyright 2026 Luca Orioli <lucaorioli@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from werkzeug.exceptions import NotFound

from odoo import http
from odoo.http import content_disposition, request


class L10nItEdiExtController(http.Controller):
    @http.route(
        "/l10n_it_edi_ext/xml_attachment/<int:move_id>/<int:index>",
        type="http",
        auth="user",
        readonly=True,
    )
    def xml_attachment(self, move_id, index, download=False):
        """Serve an <Allegati> node of the generated e-invoice XML.

        Only PDF and raster images are displayed inline (see
        account.move._l10n_it_edi_ext_xml_attachment_mimetype): the content
        of the XML is not trusted.
        """
        move = request.env["account.move"].browse(move_id).exists()
        if not move:
            raise NotFound()
        move.check_access("read")
        xml_file = move._l10n_it_edi_ext_get_xml_attachment_file(index)
        if not xml_file:
            raise NotFound()
        name, mimetype, content = xml_file
        inline = not download and mimetype != "application/octet-stream"
        return request.make_response(
            content,
            headers=[
                ("Content-Type", mimetype),
                ("Content-Length", str(len(content))),
                (
                    "Content-Disposition",
                    content_disposition(name, "inline" if inline else "attachment"),
                ),
                ("X-Content-Type-Options", "nosniff"),
            ],
        )
