# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010-2010 Camptocamp Austria (<http://www.camptocamp.at>)
#    Copyright (C) 2011
#    Associazione OpenERP Italia (<http://www.openerp-italia.org>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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

from osv import fields, osv
import decimal_precision as dp
from decimal import *

class account_tax(osv.osv):

    _inherit = 'account.tax'
    
    _columns = {
        'line_precision' : fields.boolean('Rounding Precision', help="Calculates floating point tax per line to simulate vertical calculation"),
    }
    
    _defaults = {
        'line_precision': True
    }

    def _compute(self, cr, uid, taxes, price_unit, quantity, address_id=None, product=None, partner=None):
        res = super(account_tax, self)._compute(cr, uid, taxes, price_unit, quantity, address_id, product, partner)
        tax_pool=self.pool.get('account.tax')
        total = 0.0
        for r in res:
            tax = tax_pool.browse(cr, uid, r['id'])
            if tax.line_precision:
                if r.get('balance',False):
                    r['amount'] = r.get('balance', 0.0) * quantity - total
                else:
                    r['amount'] = r.get('amount', 0.0) * quantity
                    total += r['amount']
        return res


account_tax()
