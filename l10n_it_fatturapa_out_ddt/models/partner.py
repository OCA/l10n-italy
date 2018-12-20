# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Apulia Software s.r.l. (http://www.apuliasoftware.it)
#    @author Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
##############################################################################


from openerp import fields, models


class ResPartner(models.Model):

    _inherit = 'res.partner'

    ddt_show_price = fields.Boolean(
        string='DDT show prices', default=False, help="Show prices and \
        discounts in ddt report")
