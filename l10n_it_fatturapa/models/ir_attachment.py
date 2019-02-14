# -*- coding: utf-8 -*-

import lxml.etree as ET
import re
import base64
import binascii
import logging
from io import BytesIO
from openerp.osv import fields, orm
from openerp.exceptions import Warning as UserError
from openerp.modules.module import get_module_resource
from openerp.osv.osv import except_osv
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

try:
    from asn1crypto import cms
except (ImportError, IOError) as err:
    _logger.debug(err)

re_xml = re.compile(br'(\xef\xbb\xbf)*\s*<\?xml', re.I)
re_base64 = re.compile(
    br'^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$')


class Attachment(orm.Model):
    _inherit = 'ir.attachment'

    def _compute_ftpa_preview_link(self, cr, uid, ids, context={}):
        for att in self.browse(cr, uid, ids, context):
            self.write(cr, uid, ids, {
                'ftpa_preview_link': '/fatturapa/preview/%s' % att.id
                })

    _columns = {
        'ftpa_preview_link': fields.char(
            "Preview link", readonly=True, compute=_compute_ftpa_preview_link
        )
    }

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
        try:
            info = cms.ContentInfo.load(data)
        except Exception as ex:
            logging.info('Error loading data for descript Exception: %r' % (ex))
            info = cms.ContentInfo.load(base64.b64decode(data))
        return info['content']['encap_content_info']['content'].native

    def cleanup_xml(self, xml_string):
        xml_string = self.remove_xades_sign(xml_string)
        xml_string = self.strip_xml_content(xml_string)
        return xml_string

    def get_xml_string(self, cr, uid, ids, context={}):
        fatturapa_attachment = self.browse(cr, uid, [ids], context)[0]
        try:
            data = base64.b64decode(fatturapa_attachment.datas)
        except binascii.Error as e:
            raise UserError(
                _('Corrupted attachment {}.'.format(e.args))
            )
        if re_xml.match(data) is not None:
            return self.cleanup_xml(data)
        if re_base64.match(data) is not None:
            try:
                data = base64.b64decode(data)
            except binascii.Error as e:
                raise UserError(
                    _('Base64 encoded file {}.'.format(e.args))
                )
        # Amazon sends invalid xml files, so they cannot be detected
        # using a pattern, we try to parse as asn1, if it fails
        # we assume is xml
        try:
            data = self.extract_cades(data)
        except (ValueError, KeyError):
            pass

        try:
            return self.cleanup_xml(data)
        except Exception as e:  # (AttributeError, SAXParseException)
            raise UserError(
                _('Invalid xml'.format(e.args))
            )

    def get_fattura_elettronica_preview(self):
        xsl_path = get_module_resource(
            'l10n_it_fatturapa', 'data', 'fatturaordinaria_v1.2.1.xsl')
        xslt = ET.parse(xsl_path)
        xml_string = self.get_xml_string(
            self._cr, self._uid, self._ids, self._context)
        xml_file = BytesIO(xml_string)
        recovering_parser = ET.XMLParser(recover=True)
        dom = ET.parse(xml_file, parser=recovering_parser)
        transform = ET.XSLT(xslt)
        newdom = transform(dom)
        return ET.tostring(newdom, pretty_print=True)
