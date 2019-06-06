# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models, fields
from odoo.exceptions import ValidationError


class AccountGroup(models.Model):
    _inherit = 'account.group'

    account_ids = fields.One2many(
        comodel_name='account.account',
        inverse_name='group_id',
        string="Accounts")

    @api.constrains('account_ids')
    def check_constrain_account_types(self):
        error_msg = '\n'.join([
            _("Cannot link accounts of different types to group '{}'."
              .format(group.name))
            for group in self
            if len(group.account_ids.mapped('user_type_id')) > 1
        ])
        if error_msg:
            raise ValidationError(error_msg)
