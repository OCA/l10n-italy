# Copyright 2024-2026 Innovyou srl <http://www.innovyou.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_74ter_agent = fields.Boolean(string="74ter agency")
    agent_74ter_id = fields.Many2one("res.partner", string="Agency")
    invoices_paid_by_agent = fields.Boolean()
