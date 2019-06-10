# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountGroup(models.Model):
    _inherit = 'account.group'

    account_ids = fields.One2many(
        comodel_name='account.account',
        inverse_name='group_id',
        string="Accounts",
    )
    account_balance_sign = fields.Integer(
        compute="_compute_account_balance_sign",
        string="Balance sign",
    )

    @api.constrains('account_ids')
    def check_constrain_account_types(self):
        error_msg = '\n'.join([
            _("Cannot link accounts of different types to group '{}'."
              .format(group.name))
            for group in self
            if len(group.account_ids.mapped('user_type_id').ids) > 1
        ])
        if error_msg:
            raise ValidationError(error_msg)

    @api.multi
    def _compute_account_balance_sign(self):
        for group in self:
            acc_type = group.get_first_account_type()
            if acc_type:
                group.account_balance_sign = acc_type.account_balance_sign
            else:
                group.account_balance_sign = 1

    def get_first_account_type(self):
        if self.account_ids:
            return self.account_ids[0].user_type_id
        children = self.search([('parent_id', '=', self.id)])
        for child in children:
            return child.get_first_account_type()
