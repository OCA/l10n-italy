# -*- coding: utf-8 -*-
# Copyright 2017 Simone Versienti <s.versienti@apuliasoftware.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    withholding_tax_exclude = fields.Boolean()
