# -*- coding: utf-8 -*-
# Copyright 2017 Andrea Cometa - Apulia Software
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models
from openerp.addons import decimal_precision as dp


class DdtShipmentCosts(models.Model):
    _name = 'ddt.shipment.cost'

    shipment_cost_product_id = fields.Many2one(
        'product.product', "Shipment cost product",
        help="Product used to manage shipment costs when invoicing a ddt",
    )
    lower_limit = fields.Float(
        "Lower limit", digits=dp.get_precision('Account'))
    upper_limit = fields.Float(
        "Upper limit", digits=dp.get_precision('Account'))
    company_id = fields.Many2one('res.company')


class ResCompany(models.Model):
    _inherit = 'res.company'

    shipment_cost_ids = fields.One2many(
        'ddt.shipment.cost', 'company_id', "Shipment cost product",
        help="Product used to manage shipment costs when invoicing a ddt",
    )
