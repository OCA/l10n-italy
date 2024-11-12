from odoo import models, fields


class AccountConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    payments_74ter_journal_id = fields.Many2one(
        related="company_id.payments_74ter_journal_id",
        string="Journal for agencies payments",
        readonly=False,
    )
