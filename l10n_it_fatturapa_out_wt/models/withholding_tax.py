# -*- coding: utf-8 -*-
# Author(s): Sergio Corato (https://efatto.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import fields, models


class WithholdingTax(models.Model):
    _inherit = 'withholding.tax'

    welfare_fund_type_id = fields.Many2one(
        'welfare.fund.type', 'Welfare Fund Type')
    wt_types = fields.Selection([
        ('enasarco', 'Enasarco tax'),
        ('ritenuta', 'Withholding tax'),
        ], 'Withholding tax type', required=True, default='ritenuta')
