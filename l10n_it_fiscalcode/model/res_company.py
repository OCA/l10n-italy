# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'
    fiscalcode = fields.Char(
        related='partner_id.fiscalcode', store=True, readonly=False)
