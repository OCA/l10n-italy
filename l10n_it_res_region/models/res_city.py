from odoo import api, fields, models


class City(models.Model):
    _inherit = 'res.city'

    it_region_id = fields.Many2one('res.it.region', 'Region')

    @api.onchange('it_region_id')
    def onchange_it_region_id(self):
        if self.it_region_id:
            self.country_id = self.it_region_id.country_id
