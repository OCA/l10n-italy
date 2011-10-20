# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
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

class res_company(osv.osv):

    _inherit = 'res.company'
    
    _columns = {
        'vertical_comp' : fields.boolean('Tax Vertical Calculation'),
    }
    
    _defaults = {
        'vertical_comp': True
    }

res_company()

class account_tax(osv.osv):

    _inherit = 'account.tax'

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

account_tax()
