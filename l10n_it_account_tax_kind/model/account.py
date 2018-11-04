# -*- coding: utf-8 -*-
#
#    Copyright (C) 2017 Apulia Software s.r.l. (http://www.apuliasoftware.it)
#    @author Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
#   Andrea Cometa <a.cometa@apuliasoftware.it>
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import orm, fields


class AccountTax(orm.Model):

    _inherit = 'account.tax'

    _columns = {
        'kind_id': fields.many2one('account.tax.kind', string="Kind"),
        'law_reference': fields.char(string="Law reference", size=255),
    }
