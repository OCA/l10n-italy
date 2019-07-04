#  Copyright 2019 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    tax_stamp_product_id = fields.Many2one(
        related='company_id.tax_stamp_product_id',
        string="Tax Stamp Product",
        help="Product used as Tax Stamp in customer invoices."
        )
