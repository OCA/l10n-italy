# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class Account(models.Model):
    _inherit = 'account.account'

    @api.constrains('group_id')
    def check_group_constrain_account_types(self):
        self.mapped('group_id').check_constrain_account_types()
