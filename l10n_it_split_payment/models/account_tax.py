# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class AccountTax(models.Model):
    _inherit = 'account.tax'
    is_split_payment = fields.Boolean(
        "Is split payment", compute="_compute_is_split_payment")

    @api.multi
    def _compute_is_split_payment(self):
        for tax in self:
            fp_lines = self.env['account.fiscal.position.tax'].search(
                [('tax_dest_id', '=', tax.id)])
            tax.is_split_payment = any(
                fp_line.position_id.split_payment for fp_line in fp_lines
            )
