# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011
#    Associazione OpenERP Italia (<http://www.openerp-italia.org>)
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    All Rights Reserved
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
{
    'name': 'Account Invoice Tax - Computation By Column',
    'version': '0.1',
    'category': 'Generic Modules/Accounting',
    'description': """    
    -Invoice taxes: 
        legend:
            TA(l)    TaxAmount for line l
            TBA(l)   TaxBaseAmount for line l
            TA(t)    TaxAmount for tax t
            TBA(t)   TaxBaseAmount for tax t
            
        default behaviour: 
            openerp by default calculates taxes line by line as a function of line tax base amount 
            and then groups these amounts by tax.
            TA(l) = f(TBA(l)
            TA(t) = sum( round( TA(l) ) )    /sum on lines l to which tax t is applied
        this module behaviour: 
            In Italy the correct way to compute taxes is to first compute the tax base amount TBA(t) 
            and the compute TA as a function of TBA(t)
            TBA(t) = sum( TBA(t) )    /sum on lines l to which tax t is applied
            TA(t) = f( TBA(t) )
        the result difference is small but important

    NOTE
    ====
    
    For OpenERP 6.1, please use the patch contained in the following branch:
https://code.launchpad.net/~openerp-community/openobject-addons/fix-account-6-1-tax-computation-method
instead of this module

    For OpenERP > 6.1, the fix has been merged yet:
https://code.launchpad.net/~akretion-team/openobject-addons/trunk-add-tax-rounding-option/+merge/113833
so this module is not needed anymore
    
    """,
    'author': 'OpenERP Italian Community',
    'website': 'http://www.openerp-italia.org',
    'license': 'AGPL-3',
    "depends" : ['account', 'account_voucher'],
    "init_xml" : [],
    "update_xml" : ['invoice_view.xml',],
    "demo_xml" : [],
    'test': [
        'test/account_tax.xml',
        'test/tax_computation.yml',
        ],
    "active": False,
    "installable": True
}
