from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountTax(models.Model):
    _inherit = 'account.tax'

    is_tax_74ter = fields.Boolean(
        string='74ter',
        help='Indicates that this tax is a 74ter tax',
    )

    tax_74ter_amount = fields.Float(
        string='74ter Amount',
        help='Amount of 74ter tax'
    )

    tax_74_ter_income_account_id = fields.Many2one(
        comodel_name='account.account',
        string='74ter Income Account',
        help='Income account for 74ter tax'
    )

    @api.constrains('is_tax_74ter')
    def check_multiple_debit_74ter(self):
        taxes = self.env['account.tax'].search([('is_tax_74ter', '=', True), ('type_tax_use', '=', 'sale')])
        if len(taxes) > 1:
            raise UserError(_('Only one sale tax can be 74ter.'))

    @api.constrains('tax_74ter_amount')
    def check_tax_74ter_amount(self):
        # There can only be one percentage for all 74ter taxes
        taxes = self.env['account.tax'].search([('is_tax_74ter', '=', True)])
        rates = [tax.tax_74ter_amount for tax in taxes]
        if len(set(rates)) > 1:
            raise UserError(_('All 74ter taxes must have the same rate.'))

