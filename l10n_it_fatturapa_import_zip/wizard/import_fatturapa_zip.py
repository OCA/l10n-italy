# Copyright 2015 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# Copyright 2011-2021 https://OmniaSolutions.website
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import base64
import datetime
import os
from io import BytesIO
from zipfile import ZipFile

from odoo import fields, models


class ImportFatturaPaZip(models.Model):
    _name = "import.fatturepa_zip"

    data = fields.Binary("File")

    def ImportIN(self):
        whereToExtract = os.path.join(
            "/tmp", "IN_%s" % datetime.datetime.now().strftime("%Y%m%d%H%M")
        )
        with ZipFile(BytesIO(base64.b64decode(self.data)), "r") as f:
            f.extractall(whereToExtract)
        imported_ids = self.env
        ["fatturapa.attachment.in"].get_xml_customer_invoice(whereToExtract)
        return {
            "type": "ir.actions.act_window",
            "name": "Imported Invoice",
            "res_model": "fatturapa.attachment.in",
            "view_mode": "list,form",
            "view_type": "list",
            "domain": [("id", "in", imported_ids.ids)],
        }
