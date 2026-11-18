from odoo import models, fields


class Company(models.Model):
    _inherit = "res.company"

    payments_74ter_journal_id = fields.Many2one(
        "account.journal", string="Journal for agencies payments")