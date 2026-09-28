# Copyright 2024-2026 Innovyou srl <http://www.innovyou.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    payments_74ter_journal_id = fields.Many2one(
        related="company_id.payments_74ter_journal_id",
        string="Journal for agencies payments",
        readonly=False,
    )
