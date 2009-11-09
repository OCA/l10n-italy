# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2009 Domsense SRL (<http://www.domsense.com>). 
#    All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Italy - Minimal',
    'version': '1.1',
    'category': 'Localisation/Account Charts',
    'description': """This is the base module to manage the accounting chart for Italy in Open ERP.""",
    'author': 'OpenERP Italian Community',
    'website': 'http://www.openerp-italia.org',
    "depends" : ['base', 'account', 'base_vat', 'account_chart', 'base_iban'],
    "init_xml" : [
    ],
    "update_xml" : ['account_tax_code.xml','account_chart.xml',
                    'account_tax.xml','account_chart_wizard.xml'],
    "demo_xml" : [],
    "active": False,
    "installable": True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

