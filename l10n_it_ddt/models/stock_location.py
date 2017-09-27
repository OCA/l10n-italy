# -*- coding: utf-8 -*-
# Copyright 2017 Dinamiche Aziendali s.r.l. (http://www.dinamicheaziendali.it)
# @author Gianmarco Conte <gconte@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockLocationTypeDdt(models.Model):
    _inherit = 'stock.location'

    type_ddt_id = fields.Many2one('stock.ddt.type', string='Type DDT')
