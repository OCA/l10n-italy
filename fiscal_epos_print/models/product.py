# coding=utf-8

from odoo import models, api, _
from odoo.exceptions import ValidationError


class Product(models.Model):
    _inherit = 'product.template'

    @api.constrains('available_in_pos', 'taxes_id')
    def _check_pos_prod_taxes(self):
        if self.available_in_pos:
            if len(self.taxes_id) != 1:
                raise ValidationError(
                    _("Product %s must have 1 tax") % self.display_name)
