# Copyright 2024 Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from io import BytesIO

from lxml import etree

from odoo import _, api, models, tools
from odoo.exceptions import UserError


class IrAttachmentInherit(models.Model):
    _inherit = "ir.attachment"

    @api.model
    def get_fatturapa_preview_style_name(self):
        """Hook to have a clean inheritance."""
        return "FoglioStileAssoSoftware.xsl"

    @api.model
    def remove_xades_sign(self, xml_string):
        # Recovering parser is needed for files where strings like
        # xmlns:ds="http://www.w3.org/2000/09/xmldsig#&quot;"
        # are present: even if lxml raises
        # {XMLSyntaxError}xmlns:ds:
        # 'http://www.w3.org/2000/09/xmldsig#"' is not a valid URI
        # such files are accepted by SDI
        try:
            recovering_parser = etree.XMLParser(recover=True, resolve_entities=False)
            root = etree.fromstring(xml_string, recovering_parser)
            for elem in root.iter("*"):
                if "Signature" in elem.tag:
                    elem.getparent().remove(elem)
                    break
                if any(" " in (ns_uri or "") for ns_uri in elem.nsmap.values()):
                    etree.cleanup_namespaces(elem)
            return etree.tostring(root)
        except (etree.ParseError, ValueError) as e:
            raise UserError(_(f"XML parsing of '{self.name}' failed: {str(e)}")) from e

    def get_xml_string(self):
        if not self._is_l10n_it_edi_import_file():
            raise UserError(_("Invalid xml %s.") % self.name)
        xml_string = self._decode_edi_l10n_it_edi(self.name, self.raw)[0]["content"]
        return self.remove_xades_sign(xml_string)

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
