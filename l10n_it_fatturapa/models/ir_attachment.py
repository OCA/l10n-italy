#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

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


re_base64 = re.compile(
    br'^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$')


def is_base64(s):
    s = s or b""
    s = s.replace(b"\r", b"").replace(b"\n", b"")
    return re_base64.match(s)


class FatturaPAAttachment (models.AbstractModel):
    _name = "fatturapa.attachment"
    _description = "SdI file"
    _inherits = {
        'ir.attachment': 'ir_attachment_id',
    }
    _inherit = [
        'mail.thread',
    ]
    _order = 'id desc'

    ir_attachment_id = fields.Many2one(
        comodel_name='ir.attachment',
        string='Attachment',
        required=True,
        ondelete="cascade",
    )
    att_name = fields.Char(
        string="SdI file name",
        related='ir_attachment_id.name',
        store=True,
    )
    ftpa_preview_link = fields.Char(
        "Preview link", readonly=True, compute="_compute_ftpa_preview_link"
    )

    @api.multi
    def _compute_ftpa_preview_link(self):
        for att in self:
            att.ftpa_preview_link = '/fatturapa/preview/%s' \
                                    % att.ir_attachment_id.id

    @api.model
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

    @api.model
    def strip_xml_content(self, xml):
        recovering_parser = ET.XMLParser(recover=True)
        root = ET.XML(xml, parser=recovering_parser)
        return ET.tostring(root)

    @staticmethod
    def extract_cades(data):
        info = cms.ContentInfo.load(data)
        return info['content']['encap_content_info']['content'].native

    @api.model
    def cleanup_xml(self, xml_string):
        xml_string = self.remove_xades_sign(xml_string)
        xml_string = self.strip_xml_content(xml_string)
        return xml_string

    @api.multi
    def get_xml_string(self, attachment=None):
        if not attachment:
            self.ensure_one()
            attachment = self.ir_attachment_id
        try:
            data = base64.b64decode(attachment.datas)
        except binascii.Error as e:
            raise UserError(
                _(
                    'Corrupted attachment %s.'
                ) % e.args
            )

        if is_base64(data):
            try:
                data = base64.b64decode(data)
            except binascii.Error as e:
                raise UserError(
                    _(
                        'Base64 encoded file %s.'
                    ) % e.args
                )

        # Amazon sends xml files without <?xml declaration,
        # so they cannot be easily detected using a pattern.
        # We first try to parse as asn1, if it fails we assume xml

        # asn1crypto parser will raise ValueError
        # if the asn1 cannot be parsed
        # KeyError is raised if one of the needed key is not
        # in the asn1 structure (info->content->encap_content_info->content)
        try:
            data = self.extract_cades(data)
        except (ValueError, KeyError):
            pass

        try:
            return self.cleanup_xml(data)
        # cleanup_xml calls root.iter(), but root is None if the parser fails
        # Invalid xml 'NoneType' object has no attribute 'iter'
        except AttributeError as e:
            raise UserError(
                _(
                    'Invalid xml %s.'
                ) % e.args
            )

    @api.model
    def get_fattura_elettronica_preview(self, attachment):
        company = self.env.user.company_id
        xsl_path = get_module_resource(
            'l10n_it_fatturapa', 'data',
            company.fatturapa_preview_style)
        xslt = ET.parse(xsl_path)
        xml_string = self.get_xml_string(attachment)
        xml_file = BytesIO(xml_string)
        recovering_parser = ET.XMLParser(recover=True)
        dom = ET.parse(xml_file, parser=recovering_parser)
        transform = ET.XSLT(xslt)
        newdom = transform(dom)
        return ET.tostring(newdom, pretty_print=True)
