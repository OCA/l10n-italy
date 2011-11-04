# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>). 
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

class account_tax_code(osv.osv):

    _inherit = 'account.tax.code'
    _columns = {
        'tax_ids': fields.one2many('account.tax', 'tax_code_id', 'Taxes'),
        'base_tax_ids': fields.one2many('account.tax', 'base_code_id', 'Base Taxes'),
        }

account_tax_code()

class account_invoice_tax(osv.osv):

    _inherit = 'account.tax'
    _columns = {
        'exclude_from_registries': fields.boolean('Exclude from VAT registries'),
        'base_tax_ids': fields.one2many('account.tax', 'base_code_id', 'Base Taxes'),
        }
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'The tax name must be unique!'),
    ]

    def get_main_tax(self, tax):
        if not tax.parent_id:
            return tax
        else:
            return self.get_main_tax(tax.parent_id)

    def get_account_tax(self, cr, uid, inv_tax_name):
        splitted_name = inv_tax_name.split(' - ')
        if len(splitted_name) > 1:
            tax_name = splitted_name[1]
        else:
            tax_name = splitted_name[0]
        # cerco la tassa per nome, dopo averlo ottenuto dalla tassa in fattura
        tax_ids = self.search(cr, uid, [('name', '=', tax_name)])
        if not tax_ids:
            raise osv.except_osv(_('Error'), _('The tax %s does not exist') % tax_name)
        if len(tax_ids) > 1:
            raise osv.except_osv(_('Error'), _('Too many taxes with name %s') % tax_name)
        return self.browse(cr, uid, tax_ids[0])

account_invoice_tax()
