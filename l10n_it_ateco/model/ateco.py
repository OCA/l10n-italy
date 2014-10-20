# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Abstract
#    (<http://abstract.it>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models
from openerp import fields


class ateco_category(models.Model):
    _name = 'ateco.category'
    _description = 'ATECO Code'

    name = fields.Char(
        'Name',
        required=True
    )
    code = fields.Char(
        'ATECO Code',
        size=9,
        required=False
    )
    description = fields.Text(
        'Description'
    )
    parent_id = fields.Many2one(
        'ateco.category',
        'Parent Category',
        select=True
    )
    child_ids = fields.One2many(
        'ateco.category',
        'parent_id',
        'Child Categories'
    )
    partner_ids = fields.Many2many(
        'res.partner',
        'ateco_category_partner_rel',
        'ateco_id',
        'partner_id',
        'Partners'
    )
