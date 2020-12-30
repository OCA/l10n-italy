# Copyright 2020 Tecnativa - Víctor Martínez
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import models, fields


class AccountTax(models.Model):
    _name = 'account.tax'
    _inherit = ['account.tax', 'l10n_it_esigibilita_iva.mixin']

    payability = fields.Selection(
        [
            ('I', 'VAT payable immediately'),
            ('D', 'unrealized VAT'),
            ('S', 'split payments'),
        ],
        string="VAT payability"
    )
