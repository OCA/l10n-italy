# -*- coding: utf-8 -*-
# © 2016 Nicola Malcontenti - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    association = fields.Boolean(
        string='Is Association', default=False)

    @api.one
    @api.onchange('association')
    def onchange_association(self):
        if self.association:
            self.is_company = True
