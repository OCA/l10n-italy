from odoo import api, models


class CityZipGeonamesImportItRegion(models.TransientModel):
    _inherit = 'city.zip.geonames.import'

    @api.model
    def prepare_city(self, row, country, state_id):
        vals = super().prepare_city(row, country, state_id)
        if row[4]:
            it_region_id = self.env['res.it.region'].search([
                ('country_id.code', '=', country.code), ('code', '=', row[4])])
            if it_region_id:
                vals['it_region_id'] = it_region_id.id
        return vals
