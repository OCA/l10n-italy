import lxml.etree as ET
import os
import base64
import shlex
import subprocess
import logging
import re
from io import BytesIO
from odoo import models, api, fields
from odoo.modules import get_module_resource
from odoo.exceptions import UserError
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class Attachment(models.Model):
    _inherit = 'ir.attachment'

    ftpa_preview_link = fields.Char(
        "Preview link", readonly=True, compute="_compute_ftpa_preview_link"
    )

    @api.multi
    def _compute_ftpa_preview_link(self):
        for att in self:
            att.ftpa_preview_link = '/fatturapa/preview/%s' % att.id

    def check_file_is_pem(self, p7m_file):
        file_is_pem = True
        strcmd = (
            'openssl asn1parse  -inform PEM -in %s'
        ) % (p7m_file)
        cmd = shlex.split(strcmd)
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            proc.communicate()
            if proc.wait() != 0:
                file_is_pem = False
        except Exception as e:
            raise UserError(
                _(
                    "An error with command 'openssl asn1parse' occurred: %s."
                ) % e.args
            )
        return file_is_pem

    def parse_pem_2_der(self, pem_file, tmp_der_file):
        strcmd = (
            'openssl asn1parse -in %s -out %s'
        ) % (pem_file, tmp_der_file)
        cmd = shlex.split(strcmd)
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            stdoutdata, stderrdata = proc.communicate()
            if proc.wait() != 0:
                _logger.warning(stdoutdata)
                raise Exception(stderrdata)
        except Exception as e:
            raise UserError(
                _(
                    'Parsing PEM to DER file %s.'
                ) % e.args
            )
        if not os.path.isfile(tmp_der_file):
            raise UserError(
                _(
                    'ASN.1 structure is not parsable in DER.'
                )
            )
        return tmp_der_file

    # Due to a (likely) openssl bug (v.1.1.0x) we need to decrypt
    # files without message signature verification (-nosigs option).
    # Otherwise openssl gives an error like the following one on
    # some files (decrypted anyway):
    #
    # Verification failure
    # int_rsa_verify:bad signature
    # PKCS7_signatureVerify:signature failure
    # PKCS7_verify:signature failure
    #
    # Tested openssl versions:
    # 1.0.1t-1+deb8u8    - Debian 8     - OK
    # 1.0.2g-1ubuntu4.14 - Ubuntu 16.04 - OK
    # 1.1.0f-3+deb9u2    - Debian 9     - affected
    # 1.1.0g-2ubuntu4.3  - Ubuntu 18.04 - affected

    def decrypt_to_xml(self, signed_file, xml_file):
        strcmd = (
            'openssl smime -decrypt -verify -inform'
            ' DER -in %s -noverify -nosigs -out %s'
        ) % (signed_file, xml_file)
        cmd = shlex.split(strcmd)
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            stdoutdata, stderrdata = proc.communicate()
            if proc.wait() != 0:
                _logger.warning(stdoutdata)
                raise Exception(stderrdata)
        except Exception as e:
            raise UserError(
                _(
                    'Signed Xml file %s.'
                ) % e.args
            )
        if not os.path.isfile(xml_file):
            raise UserError(
                _(
                    'Signed Xml file not decryptable.'
                )
            )
        return xml_file

    def remove_xades_sign(self, xml):
        root = ET.XML(xml)
        for elem in root.iter('*'):
            if elem.tag.find('Signature') > -1:
                elem.getparent().remove(elem)
                break
        return ET.tostring(root)

    def strip_xml_content(self, xml):
        root = ET.XML(xml)
        for elem in root.iter('*'):
            if elem.text is not None:
                elem.text = elem.text.strip()
        return ET.tostring(root)

    def isBase64(self, s):
        prog = re.compile(
            b"^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$"
        )
        if prog.match(s):
            return True
        return False

    def get_xml_string(self):
        fatturapa_attachment = self
        # decrypt  p7m file
        if fatturapa_attachment.datas_fname.lower().endswith('.p7m'):
            temp_file_name = (
                '/tmp/%s' % fatturapa_attachment.datas_fname.lower())
            temp_der_file_name = (
                '/tmp/%s_tmp' % fatturapa_attachment.datas_fname.lower())
            with open(temp_file_name, 'wb') as p7m_file:
                datas = fatturapa_attachment.datas
                format_data = base64.decodebytes(datas)
                if self.isBase64(format_data):
                    format_data = base64.b64decode(format_data)
                p7m_file.write(format_data)
            xml_file_name = os.path.splitext(temp_file_name)[0]

            # check if temp_file_name is a PEM file
            file_is_pem = self.check_file_is_pem(temp_file_name)

            # if temp_file_name is a PEM file
            # parse it in a DER file
            if file_is_pem:
                temp_file_name = self.parse_pem_2_der(
                    temp_file_name, temp_der_file_name)

            # decrypt signed DER file in XML readable
            xml_file_name = self.decrypt_to_xml(
                temp_file_name, xml_file_name)

            with open(xml_file_name, 'rb') as fatt_file:
                file_content = fatt_file.read()
            xml_string = file_content
        elif fatturapa_attachment.datas_fname.lower().endswith('.xml'):
            xml_string = base64.decodebytes(fatturapa_attachment.datas)
        xml_string = self.remove_xades_sign(xml_string)
        xml_string = self.strip_xml_content(xml_string)
        return xml_string

    def get_fattura_elettronica_preview(self):
        xsl_path = get_module_resource(
            'l10n_it_fatturapa', 'data', 'fatturaordinaria_v1.2.1.xsl')
        xslt = ET.parse(xsl_path)
        xml_string = self.get_xml_string()
        xml_file = BytesIO(xml_string)
        dom = ET.parse(xml_file)
        transform = ET.XSLT(xslt)
        newdom = transform(dom)
        return ET.tostring(newdom, pretty_print=True)
