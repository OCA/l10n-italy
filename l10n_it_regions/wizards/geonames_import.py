# -*- coding: utf-8 -*-
# Copyright 2016 Davide Corio - Abstract srl
# Copyright 2017 Andrea Cometa - Apulia Software srl
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, api


class better_zip_geonames_import(models.TransientModel):
    _inherit = 'better.zip.geonames.import'

    @api.model
    def select_or_create_state(
        self, row, country_id, code_row_index=4, name_row_index=3
    ):
        res = super(better_zip_geonames_import, self).select_or_create_state(
            row, country_id, code_row_index=6, name_row_index=5)

        region_model = self.env['res.country.region']
        region = region_model.search([('code', '=', row[4])])
        if not region:
            region = region_model.create(
                {'code': row[4], 'name': row[3]})
        res.region_id = region.id
        return res
