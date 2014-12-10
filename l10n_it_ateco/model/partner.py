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
from openerp import api
from openerp import exceptions
from openerp import fields
from openerp import models
from openerp import _


class res_partner_ateco(models.Model):
    _name = 'res.partner.ateco'

    ateco_category_id = fields.Many2one(
        'ateco.category',
        'Ateco category'
    )

    ateco_category_code = fields.Char(
        related="ateco_category_id.code",
        string="Ateco code"
    )

    partner_id = fields.Many2one(
        'res.partner',
        'Partner'
    )

    main_category = fields.Boolean("Main category")

    @api.multi
    def name_get(self):
        """Return ateco.category.complete_name"""
        return [(i.id, i.ateco_category_id.complete_name) for i in self]

    def get_main_category(self, partner_id):
        """Return the category with main_category flag set true"""
        return self.search([
            '&',
            ('partner_id', '=', partner_id),
            ('main_category', '=', True),
        ])


class res_partner(models.Model):
    _inherit = 'res.partner'

    ateco_category_ids = fields.One2many(
        "res.partner.ateco",
        "partner_id",
        "Ateco categories"
    )

    main_ateco_category_id = fields.Many2one(
        "res.partner.ateco",
        string="Main Ateco category",
        compute='_get_main_ateco_category_id'
    )

    def _get_main_ateco_category_id(self):
        """Search into res.partner.ateco related to this partner
        and get the one with main_category flag to true
        """
        ateco_obj = self.env['res.partner.ateco']
        for i in self:
            cat = ateco_obj.get_main_category(i.id)
            i.main_ateco_category_id = cat.id

    @api.one
    @api.constrains('ateco_category_ids')
    def main_category_constraint(self):
        """It is allowed only one and at least
        main ateco category for each partner"""

        # check only if there is at least one ateco category
        if len(self.ateco_category_ids) == 0:
            return

        res = [i for i in self.ateco_category_ids if i.main_category is True]
        count_rs = len(res)
        if count_rs > 1:
            raise exceptions.Warning(
                _(u"You can define only one main ateco category for a partner")
            )

        if count_rs == 0:
            raise exceptions.Warning(
                _(u"You should define at least one main ateco category")
            )
