# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import openerp.addons.decimal_precision as dp

from openerp import fields, models, api, exceptions, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.constrains('stamp_apply_tax_code_ids', 'is_stamp')
    def _check_stamp_apply_tax(self):
        for template in self:
            if template.stamp_apply_tax_code_ids and not template.is_stamp:
                raise exceptions.ValidationError(
                    _("The product %s must be a stamp to set apply taxes!")
                    % template.name)

    stamp_apply_tax_code_ids = fields.Many2many(
        'account.tax.code',
        'product_stamp_account_tax_code_rel',
        'product_id', 'tax_code_id', string='Stamp tax codes')
    stamp_apply_min_total_base = fields.Float(
        'Stamp apply min total base',
        digits=dp.get_precision('Account'))
    is_stamp = fields.Boolean('Is stamp')
