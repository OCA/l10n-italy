# -*- coding: utf-8 -*-

from openerp import models, fields


class WithholdingTax(models.Model):
    _inherit = 'withholding.tax'
    causale_pagamento_id = fields.Many2one(
        'causale.pagamento', string="Causale pagamento")
