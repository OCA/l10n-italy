# -*- coding: utf-8 -*-

from openerp import models, fields


class AccountTaxCode(models.Model):
    _inherit = 'account.tax.code'

    base_tax_ids = fields.One2many(
        'account.tax', 'base_code_id', 'Base Taxes')
    tax_ids = fields.One2many(
        'account.tax', 'tax_code_id', 'Taxes')
