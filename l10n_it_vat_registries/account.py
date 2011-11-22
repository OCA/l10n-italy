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
        'ref_tax_ids': fields.one2many('account.tax', 'ref_tax_code_id', 'Ref Taxes'),
        'ref_base_tax_ids': fields.one2many('account.tax', 'ref_base_code_id', 'Ref Base Taxes'),
        }

account_tax_code()

class account_invoice_tax(osv.osv):

    _inherit = 'account.tax'
    _columns = {
        'exclude_from_registries': fields.boolean('Exclude from VAT registries'),
        'base_tax_ids': fields.one2many('account.tax', 'base_code_id', 'Base Taxes'), # serve ancora?
        }
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'The tax name must be unique!'),
    ]

account_invoice_tax()
