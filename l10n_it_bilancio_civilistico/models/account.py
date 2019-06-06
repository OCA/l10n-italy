from odoo import models, fields


class AccountGroupCEE(models.Model):
    _inherit = "account.group"
    cee_group = fields.Boolean("Civil code group")


class Account(models.Model):
    _inherit = 'account.account'
    cee_group_id = fields.Many2one('account.group', string="Civil code group")
