from odoo import fields, models


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'
    pos_tickets_number = fields.Integer('POS tickets number', readonly=True)
