# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from io import BytesIO

from lxml import etree

from odoo import api, models, tools
from odoo.exceptions import UserError

from odoo.addons.l10n_it_edi.tools.remove_signature import remove_signature

_logger = logging.getLogger(__name__)


class IrAttachmentInherit(models.Model):
    _inherit = "ir.attachment"

    @api.model
    def get_fatturapa_preview_style_name(self):
        """Hook to have a clean inheritance."""
        return "FoglioStileAssoSoftware.xsl"

    def get_xml_string(self):
        if not self._is_l10n_it_edi_import_file():
            raise UserError(self.env._("Invalid xml %s.") % self.name)

        # from _decode_edi_l10n_it_edi()
        # for files with a Cades signature, _decode_edi_l10n_it_edi() returns the
        # orginal (signed) contents and a list of etree subtrees, each starting
        # from FatturaElettronicaBody, neither of which is useful to us here
        #
        # so we copy the code snipped that's useful to us
        # 8<
        def parse_xml(parser, name, content):
            try:
                return etree.fromstring(content, parser)
            except (etree.ParseError, ValueError) as e:
                _logger.info("XML parsing of %s failed: %s", name, e)

        name = self.name
        content = self.raw
        parser = etree.XMLParser(recover=True, resolve_entities=False)
        if (xml_tree := parse_xml(parser, name, content)) is None:
            # The file may have a Cades signature, trying to remove it
            if (xml_tree := parse_xml(parser, name, remove_signature(content))) is None:
                _logger.info("Italian EDI invoice file %s cannot be decoded.", name)
                return []
        # >8

        xml_string = etree.tostring(
            xml_tree, pretty_print=True, encoding="unicode"
        ).encode()
        return xml_string

    def get_fattura_elettronica_preview(self):
        xsl_path = tools.misc.file_path(
            f"l10n_it_edi_extension/data/{self.get_fatturapa_preview_style_name()}"
        )
        xslt = etree.parse(xsl_path)
        xml_string = self.sudo().get_xml_string()
        xml_file = BytesIO(xml_string)
        recovering_parser = etree.XMLParser(recover=True, resolve_entities=False)
        dom = etree.parse(xml_file, parser=recovering_parser)
        transform = etree.XSLT(xslt)
        newdom = transform(dom)
        return etree.tostring(newdom, pretty_print=True, encoding="unicode")
