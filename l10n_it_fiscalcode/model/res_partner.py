# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def check_fiscalcode(self):
        for partner in self:
            if not partner.fiscalcode:
                return True
            elif (
                len(partner.fiscalcode) != 16 and
                partner.company_type == 'person'
            ):
                return False
            else:
                return True

    fiscalcode = fields.Char(
        'Fiscal Code', size=16, help="Italian Fiscal Code")

    _constraints = [
        (check_fiscalcode,
         "The fiscal code doesn't seem to be correct.", ["fiscalcode"])
    ]
