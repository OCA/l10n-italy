from odoo import api, models, _
from odoo.exceptions import ValidationError
from stdnum.eu.vat import compact
from stdnum.exceptions import InvalidComponent


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
        try:
            vat_normalized = compact(self.vat)[2:]
        except InvalidComponent:
            raise ValidationError(
                _("%s is not a EU valid VAT!") % self.vat)
        if vat_normalized != res:
            res = vat_normalized
        return res
