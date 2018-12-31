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
from tools.translate import _

class account_tax(osv.osv):

    _inherit = 'account.tax'
    
    def _have_same_rate(self, account_taxes):
        rate = None
        for account_tax in account_taxes:
            if rate is None:
                rate = account_tax.amount
            elif rate != account_tax.amount:
                return False
        return True

    def get_main_tax(self, tax):
        if not tax.parent_id:
            return tax
        else:
            return self.get_main_tax(tax.parent_id)
    
    def get_account_tax_by_tax_code(self, tax_code):
        if tax_code.tax_ids:
            if not self._have_same_rate(tax_code.tax_ids):
                raise osv.except_osv(_('Error'),
                    _('The taxes %s have different rates') % str(tax_code.tax_ids))
            return tax_code.tax_ids[0]
        if tax_code.ref_tax_ids:
            if not self._have_same_rate(tax_code.ref_tax_ids):
                raise osv.except_osv(_('Error'),
                    _('The taxes %s have different rates') % str(tax_code.ref_tax_ids))
            return tax_code.ref_tax_ids[0]
        raise osv.except_osv(_('Error'),
            _('No taxes associated to tax code %s') % str(tax_code.name))
    
    def get_account_tax_by_base_code(self, tax_code):
        if tax_code.base_tax_ids:
            if not self._have_same_rate(tax_code.base_tax_ids):
                raise osv.except_osv(_('Error'),
                    _('The taxes %s have different rates') % str(tax_code.base_tax_ids))
            return tax_code.base_tax_ids[0]
        if tax_code.ref_base_tax_ids:
            if not self._have_same_rate(tax_code.ref_base_tax_ids):
                raise osv.except_osv(_('Error'),
                    _('The taxes %s have different rates') % str(tax_code.ref_base_tax_ids))
            return tax_code.ref_base_tax_ids[0]
        raise osv.except_osv(_('Error'),
            _('No taxes associated to tax code %s') % str(tax_code.name))

    def get_account_tax(self, inv_tax):
        if inv_tax.tax_code_id:
            return self.get_account_tax_by_tax_code(inv_tax.tax_code_id)
        if inv_tax.base_code_id:
            return self.get_account_tax_by_base_code(inv_tax.base_code_id)
        raise osv.except_osv(_('Error'),
            _('No tax codes for invoice tax %s') % str(inv_tax.name))

    '''
    def old_get_account_tax(self, cr, uid, inv_tax_name):
        splitted_name = inv_tax_name.split(' - ')
        if len(splitted_name) > 1:
            tax_name = splitted_name[1]
        else:
            tax_name = splitted_name[0]
        # search for tax by name, after getting it from invoice tax
        tax_ids = self.search(cr, uid, [('name', '=', tax_name)])
        if not tax_ids:
            raise osv.except_osv(_('Error'), _('The tax %s does not exist') % tax_name)
        if len(tax_ids) > 1:
            raise osv.except_osv(_('Error'), _('Too many taxes with name %s') % tax_name)
        return self.browse(cr, uid, tax_ids[0])
    '''

account_tax()

class account_tax_code(osv.osv):

    _inherit = 'account.tax.code'
    
    _columns = {
        'base_tax_ids': fields.one2many('account.tax', 'base_code_id', 'Base Taxes'),
        'tax_ids': fields.one2many('account.tax', 'tax_code_id', 'Taxes'),
        'ref_base_tax_ids': fields.one2many('account.tax', 'ref_base_code_id', 'Ref Base Taxes'),
        'ref_tax_ids': fields.one2many('account.tax', 'ref_tax_code_id', 'Ref Taxes'),
        }

account_tax_code()
