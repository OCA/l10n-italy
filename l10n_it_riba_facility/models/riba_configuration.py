# Copyright 2026 Nextev
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class RibaConfiguration(models.Model):
    _inherit = "riba.configuration"

    riba_facility_amount = fields.Float(
        string="Bank Receipts Facility",
        digits="Account",
        help="Credit line for RiBa SBF advances granted on this bank account.",
    )
