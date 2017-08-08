# -*- coding: utf-8 -*-
# Copyright © 2015 Alessandro Camilli (<http://www.openforce.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    income_type_id = fields.Many2one(
        'withholding.tax.income.type', string='Income Type Partner')
