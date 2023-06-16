from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    it_region_id = fields.Many2one('res.it.region', compute='_compute_address',
                                   inverse='_inverse_region',
                                   string="Region")

    def _get_company_address_fields(self, partner):
        res = super()._get_company_address_fields(partner)
        res['it_region_id'] = partner.it_region_id
        return res

    def _inverse_region(self):
        for company in self:
            company.with_context(
                skip_check_zip=True).partner_id.it_region_id = company.it_region_id

    @api.onchange('it_region_id')
    def _onchange_region(self):
        self.country_id = self.it_region_id.country_id

    @api.onchange('zip_id')
    def _onchange_zip_id(self):
        if self.zip_id:
            super()._onchange_zip_id()
            self.it_region_id = self.zip_id.city_id.it_region_id
