# -*- coding: utf-8 -*-
# © <2016> <Nicola Malcontenti - nicola.malcontenti@agilebg.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class Company(models.Model):
    _inherit = 'res.company'

    check_purchase_tax_multicompany = fields.Boolean(
        string='Check Purchase Tax Multicompany',
        help='Check this field to allow this company\n'
             ' to use purchase tax in multicompany')
