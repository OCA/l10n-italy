from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    it_region_id = fields.Many2one("res.it.region",
                                   string='Region',
                                   ondelete='restrict')

    @api.onchange('zip_id')
    def _onchange_zip_id(self):
        super()._onchange_zip_id()
        if self.zip_id and self.zip_id.city_id.it_region_id:
            self.it_region_id = self.zip_id.city_id.it_region_id

    @api.constrains('zip_id', 'country_id', 'city_id', 'state_id', 'it_region_id')
    def _check_zip(self):
        super()._check_zip()
        if self.env.context.get('skip_check_zip'):
            return
        for rec in self:
            if not rec.zip_id:
                continue
            if rec.zip_id.city_id.it_region_id != rec.it_region_id:
                raise ValidationError(_(
                    "The region of the partner %s differs from that in "
                    "location %s") % (rec.name, rec.zip_id.name))

    @api.onchange('it_region_id')
    def _onchange_it_region_id(self):
        vals = {}
        if self.it_region_id.country_id:
            vals.update({'country_id': self.it_region_id.country_id})
        if self.zip_id and self.it_region_id != self.zip_id.city_id.it_region_id:
            vals.update({
                'zip_id': False,
                'zip': False,
                'city': False,
            })
        self.update(vals)

    @api.model
    def _address_fields(self):
        """Returns the list of address fields that are synced from the parent."""
        res = super()._address_fields()
        res += ['it_region_id']
        return res
