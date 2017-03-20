# -*- coding: utf-8 -*-
# Copyright 2017 Andrea Cometa - Apulia Software
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    no_shipping_costs = fields.Boolean(
        "No shipping costs",
        help="This partner has no shipping costs",
    )
