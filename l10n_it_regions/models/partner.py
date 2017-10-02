# -*- coding: utf-8 -*-
# Copyright 2016 Davide Corio - Abstract srl
# Copyright 2017 Andrea Cometa - Apulia Software srl
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    region_id = fields.Many2one('res.country.region', 'Region')

    @api.multi
    @api.onchange('zip_id')
    def onchange_zip_id(self):
        super(ResPartner, self).onchange_zip_id()
        for partner in self:
            if (partner.zip_id and partner.zip_id.state_id and
                    partner.zip_id.state_id.region_id):
                partner.region_id = partner.zip_id.state_id.region_id.id
