from odoo import models, fields


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    invoice_number = fields.Char()
