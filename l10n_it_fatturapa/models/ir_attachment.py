# -*- coding: utf-8 -*-

import lxml.etree as ET
import re
import base64
import binascii
import logging
from io import BytesIO
from odoo import models, api, fields
from odoo.modules import get_module_resource
from odoo.exceptions import UserError
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)

try:
    from asn1crypto import cms
except (ImportError, IOError) as err:
    _logger.debug(err)


re_xml = re.compile(br'(\xef\xbb\xbf)*\s*<\?xml', re.I)
re_base64 = re.compile(
    br'^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$')


class Attachment(models.Model):
    _inherit = 'ir.attachment'

    ftpa_preview_link = fields.Char(
        "Preview link", readonly=True, compute="_compute_ftpa_preview_link"
    )

    @api.multi
    def _compute_ftpa_preview_link(self):
        for att in self:
            att.ftpa_preview_link = '/fatturapa/preview/%s' % self.id

    def remove_xades_sign(self, xml):
        # Recovering parser is needed for files where strings like
        # xmlns:ds="http://www.w3.org/2000/09/xmldsig#&quot;"
        # are present: even if lxml raises
        # {XMLSyntaxError}xmlns:ds:
        # 'http://www.w3.org/2000/09/xmldsig#"' is not a valid URI
        # such files are accepted by SDI
        recovering_parser = ET.XMLParser(recover=True)
        root = ET.XML(xml, parser=recovering_parser)
        for elem in root.iter('*'):
            if elem.tag.find('Signature') > -1:
                elem.getparent().remove(elem)
                break
        return ET.tostring(root)

    def strip_xml_content(self, xml):
        recovering_parser = ET.XMLParser(recover=True)
        root = ET.XML(xml, parser=recovering_parser)
        for elem in root.iter('*'):
            if elem.text is not None:
                elem.text = elem.text.strip()
        return ET.tostring(root)

    @staticmethod
    def extract_cades(data):
        info = cms.ContentInfo.load(data)
        return info['content']['encap_content_info']['content'].native

    def cleanup_xml(self, xml_string):
        xml_string = self.remove_xades_sign(xml_string)
        xml_string = self.strip_xml_content(xml_string)
        return xml_string

    def get_xml_string(self):
        try:
            data = base64.b64decode(self.datas)
        except binascii.Error as e:
            raise UserError(
                _(
                    'Corrupted attachment %s.'
                ) % e.args
            )

        if re_xml.match(data) is not None:
            return self.cleanup_xml(data)

        if re_base64.match(data) is not None:
            try:
                data = base64.b64decode(data)
            except binascii.Error as e:
                raise UserError(
                    _(
                        'Base64 encoded file %s.'
                    ) % e.args
                )

        try:
            return self.cleanup_xml(self.extract_cades(data))
        except (ValueError, KeyError) as e:
            raise UserError(
                _(
                    'Signed Xml file %s.'
                ) % e.args
            )

    def get_fattura_elettronica_preview(self):
        xsl_path = get_module_resource(
            'l10n_it_fatturapa', 'data', 'fatturaordinaria_v1.2.1.xsl')
        xslt = ET.parse(xsl_path)
        xml_string = self.get_xml_string()
        xml_file = BytesIO(xml_string)
        recovering_parser = ET.XMLParser(recover=True)
        dom = ET.parse(xml_file, parser=recovering_parser)
        transform = ET.XSLT(xslt)
        newdom = transform(dom)
        return ET.tostring(newdom, pretty_print=True)
