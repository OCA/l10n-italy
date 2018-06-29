# -*- coding: utf-8 -*-
# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class SaleCommission(models.Model):
    _inherit = 'sale.commission'

    only_paid_riba = fields.Boolean(
        help='Include only paid RiBas', default=True)
