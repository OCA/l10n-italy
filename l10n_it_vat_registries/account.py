# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011-2012 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>). 
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv

class account_tax(osv.osv):

    _inherit = 'account.tax'
    _columns = {
        'exclude_from_registries': fields.boolean('Exclude from VAT registries'),
        'base_tax_ids': fields.one2many('account.tax', 'base_code_id', 'Base Taxes'), # serve ancora?
        }
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'The tax name must be unique!'),
    ]

    def get_account_tax(self, inv_tax):
        if inv_tax.tax_code_id:
            return self.get_account_tax_by_tax_code(inv_tax.tax_code_id)
        if inv_tax.base_code_id:
            return self.get_account_tax_by_base_code(inv_tax.base_code_id)
        raise osv.except_osv(_('Error'),
            _('No tax codes for invoice tax %s') % str(inv_tax.name))

