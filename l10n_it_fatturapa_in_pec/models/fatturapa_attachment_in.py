# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
import zipfile
import os
import re
import base64
from odoo import api, tools, exceptions, models, _
from odoo.tools import config
from odoo.addons.l10n_it_fatturapa_in_pec.models.mail import \
    RESPONSE_MAIL_REGEX


class FatturaPAAttachmentIn(models.Model):
    _inherit = "fatturapa.attachment.in"

    @api.multi
    def parse_pec_attachment(self, attachment_ids):
        regex = re.compile(RESPONSE_MAIL_REGEX)
        path = os.path.join(config['data_dir'], "filestore",
                            self.env.cr.dbname)
        for attachment in self.env['ir.attachment'].browse(
                [att_id for model, att_id in attachment_ids]):
            if regex.match(attachment.name):
                zip_path = os.path.join(path, attachment.store_fname)
                if zipfile.is_zipfile(zip_path):
                    zf = zipfile.ZipFile(zip_path)
                    for inv_file_name in zf.namelist():
                        inv_file = zf.open(inv_file_name)
                        if regex.match(inv_file_name):
                            fatturapa_in = self.create({
                                'name': inv_file_name,
                                'datas_fname': inv_file_name,
                                'datas': base64.encodestring(
                                    inv_file.read())})
                else:
                    fatturapa_in = self.create({
                        'ir_attachment_id': attachment.id})
        return True
