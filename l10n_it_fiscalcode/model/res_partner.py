# -*- coding: utf-8 -*-
# Copyright 2014 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# Copyright 2016 Andrea Gallina (Apulia Software)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def check_fiscalcode(self):
        for partner in self:
            if not partner.fiscalcode:
                return True
            elif len(partner.fiscalcode) != 16 and partner.individual:
                return False
            else:
                return True

    fiscalcode = fields.Char(
        'Fiscal Code', size=16, help="Italian Fiscal Code")
    individual = fields.Boolean(
        'Individual', default=False,
        help="If checked the C.F. is referred to a Individual Person")

    _constraints = [
        (check_fiscalcode,
         "The fiscal code doesn't seem to be correct.", ["fiscalcode"])
    ]
