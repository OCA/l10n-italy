# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class AccountTax(models.Model):

    _inherit = 'account.tax'

    kind_id = fields.Many2one('account.tax.kind', string="Exemption Kind")
    law_reference = fields.Char('Law reference')
