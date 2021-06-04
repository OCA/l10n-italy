import re

from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def format_vat_it(self, vat):
        return vat and re.sub(r"\W+", "", vat).upper() or False
