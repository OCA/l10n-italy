# -*- coding: utf-8 -*-
# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProductProduct(models.Model):

    _inherit = 'product.product'

    @api.model
    def _convert_prepared_anglosaxon_line(self, line, partner):
        res = super(ProductProduct, self)._convert_prepared_anglosaxon_line(
            line, partner)
        if line.get('force_dichiarazione_intento_id', False):
            res['force_dichiarazione_intento_id'] = line[
                'force_dichiarazione_intento_id']
        return res
