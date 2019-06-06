from odoo import models, fields


class AccountGroupCEE(models.Model):
    _inherit = "account.group"
    cee_group = fields.Boolean("Civil code group")
    cee_account_ids = fields.One2many(
        comodel_name='account.account',
        inverse_name='cee_group_id',
        string="CEE accounts")

    def get_first_account_type(self):
        if self.cee_group:
            if self.cee_account_ids:
                return self.cee_account_ids[0].user_type_id
            children = self.search([('parent_id', '=', self.id)])
            for child in children:
                if child.cee_account_ids:
                    return child.get_first_account_type()
            # In case of any valid children,
            # Increase level of children
            if children:
                sub_children = self.env['account.group']
                for child in children:
                    sub_children += self.search([
                        ('parent_id', '=', child.id),
                        ('cee_account_ids', '!=', False)
                        ])
                for child in sub_children:
                    return child.get_first_account_type()
        else:
            super(AccountGroupCEE, self).get_first_account_type()


class Account(models.Model):
    _inherit = 'account.account'
    cee_group_id = fields.Many2one('account.group', string="Civil code group")
