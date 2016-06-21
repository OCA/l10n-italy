# -*- coding: utf-8 -*-
# © 2016 Nicola Malcontenti - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    association = fields.Boolean(
        string='Is Association', default=False)
    company_type = fields.Selection(
        selection_add=[
            ('association', 'Association')])

    @api.multi
    def on_change_company_type(self, company_type):
        return_dict = {}
        res = super(
            ResPartner, self).on_change_company_type(company_type)
        if company_type == "association":
            return_dict = {'is_company': True}
            return {'value': return_dict}
        else:
            return res
