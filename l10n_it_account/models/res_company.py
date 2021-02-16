# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ResCompany(models.Model):
    _inherit = 'res.company'

    def is_country_id_code_it(self):
        self.ensure_one()
        country_it = self.env.ref("base.it")
        return self.partner_id.country_id == country_it
