# Copyright 2022 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class EInvoiceLine(models.Model):
    _inherit = 'einvoice.line'

    # set unlimited digits
    unit_price = fields.Float(
        digits=(19, 8)
    )
    qty = fields.Float(
        digits=(20, 8)
    )
