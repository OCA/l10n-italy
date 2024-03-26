from odoo import fields, models
from odoo.addons.base.models.res_country import location_name_search


class ResCountryRegion(models.Model):
    _description = "Italy Country region"
    _name = 'res.it.region'
    _order = 'code'

    country_id = fields.Many2one('res.country', string='Country', required=True)
    name = fields.Char(string='Region Name', required=True, help='')
    code = fields.Char(string='Region Code', help='The region code.', required=True)

    name_search = location_name_search

    _sql_constraints = [
        ('name_code_uniq', 'unique(country_id, code)',
         'The code of the region must be unique by country !')
    ]
