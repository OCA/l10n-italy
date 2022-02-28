# Copyright 2022 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class OssYear(models.Model):
    _name = 'oss.year'
    _description = 'Subjected OSS year'
    _order = 'company_id, year desc'
    _rec_name = 'year'

    company_id = fields.Many2one('res.company', string='Company')
    year = fields.Char(required=True)
    oss_subjected = fields.Boolean()
