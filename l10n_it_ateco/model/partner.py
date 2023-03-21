# -*- coding: utf-8 -*-
#
#    Copyright (C) 2014 Abstract (<http://abstract.it>).
#    Copyright (C) 2016 Ciro Urselli (<http://www.apuliasoftware.it>).
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ResPartner(models.Model):

    _inherit = 'res.partner'

    ateco_category_ids = fields.Many2many(
        'ateco.category',
        'ateco_category_partner_rel',
        'partner_id',
        'ateco_id',
        'Ateco categories'
    )
