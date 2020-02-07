#  Copyright 2020 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner (models.Model):
    _inherit = 'res.partner'

    epos_print_fiscalcode_receipt = fields.Boolean(
        string="Fiscal code in receipts",
        help="Print fiscal code in receipts for this partner."
    )
