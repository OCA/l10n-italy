from odoo import api, models
from stdnum.eu.vat import compact


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.multi
    def compact_vat(self):
        # VIES check is made on 'compacted' VAT with function stdnum.eu.vat.compact(),
        # so it is possibly different from VAT in this field. Make sure to set correct
        # VAT in intrastat declaration.
        self.ensure_one()
        if not self.vat:
            return False
        res = self.vat[2:]
        vat_normalized = compact(self.vat)[2:]
        if vat_normalized != res:
            res = vat_normalized
        return res
