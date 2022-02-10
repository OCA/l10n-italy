# Copyright 2021-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2021-22 Didotech s.r.l. <https://www.didotech.com>
# Copyright 2021-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    def compute_civilistico(self):
        internal_sequence = self.env['ir.model.data'].search([
            ('model', '=', 'asset.depreciation.type'),
            ('name', '=', 'ad_type_civilistico')
        ])
        return internal_sequence.res_id

    def compute_fiscale(self):
        internal_sequence = self.env['ir.model.data'].search([
            ('model', '=', 'asset.depreciation.type'),
            ('name', '=', 'ad_type_fiscale')
        ])
        return internal_sequence.res_id

    def compute_gestionale(self):
        internal_sequence = self.env['ir.model.data'].search([
            ('model', '=', 'asset.depreciation.type'),
            ('name', '=', 'ad_type_gestionale')
        ])
        return internal_sequence.res_id
