# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from openerp import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    fatturapa_sale_order_data = fields.Boolean(
        'Include sale order data in e-invoice'
    )
