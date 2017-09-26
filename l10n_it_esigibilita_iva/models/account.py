# -*- coding: utf-8 -*-

from openerp import models, fields


class AccountTax(models.Model):
    _inherit = 'account.tax'

    payability = fields.Selection([
        ('I', 'Immediate payability'),
        ('D', 'Deferred payability'),
        ('S', 'Split payment'),
    ], string="VAT payability")
