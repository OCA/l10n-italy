# Copyright 2018 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):

    _inherit = 'res.company'

    dichiarazione_yearly_limit_ids = fields.One2many(
        'dichiarazione.intento.yearly.limit', 'company_id',
        string="Declaration yearly limit")
