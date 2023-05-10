# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    cuc = fields.Char(
        string="CUC Code",
        size=35,
        help="Unique CBI code provided by your bank",
    )
