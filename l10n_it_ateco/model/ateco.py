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
from openerp import api
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

    complete_name = fields.Char(
        compute="_get_complete_name",
        string="Complete name"
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

    partner_ids = fields.One2many(
        'res.partner.ateco',
        'ateco_category_id',
        'Partners'
    )

    def _get_complete_name(self):
        """Concatenate code and name fields"""
        for res in self:
            code = res.code
            if code:
                name = u"{} - {}".format(code, res.name)
            else:
                name = res.name
            res.complete_name = name

    @api.multi
    def name_get(self):
        return [(i.id, i.complete_name) for i in self]

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        """Search in name and code fields"""
        args = args or []
        if name:
            recs = self.search([
                '|',
                ('code', operator, name),
                ('name', operator, name)
            ] + args, limit=limit)
        else:
            recs = self.browse()
        return recs.name_get()
