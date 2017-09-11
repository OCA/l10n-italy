# -*- coding: utf-8 -*-
#
#    Copyright (C) 2017 Apulia Software s.r.l. (http://www.apuliasoftware.it)
#    @author Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class AccountTax(models.Model):

    _inherit = 'account.tax'

    kind_id = fields.Many2one('account.tax.kind', string="Kind")
