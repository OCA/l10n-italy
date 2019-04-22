# -*- coding: utf-8 -*-

from odoo import models, fields


class MoveLine(models.Model):
    _inherit = 'account.move.line'
    exclude_from_vat_statement_amount = fields.Boolean(
        "Exclude from VAT statement amount", readonly=True)
