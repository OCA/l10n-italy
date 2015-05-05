# -*- coding: utf-8 -*-
# Copyright 2016 Davide Corio - Abstract srl
# Copyright 2017 Andrea Cometa - Apulia Software srl
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ResCountryRegion(models.Model):
    _name = 'res.country.region'
    _description = 'Region'

    name = fields.Char('Name')
    code = fields.Char('Code')


class ResCountryState(models.Model):
    _inherit = 'res.country.state'

    region_id = fields.Many2one('res.country.region', 'Region')
