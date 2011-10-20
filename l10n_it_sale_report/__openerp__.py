# -*- coding: utf-8 -*-
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
{
    'name': 'Italian Localisation - Sale reports',
    'version': '0.1',
    'category': 'Localisation/Italy',
    'description': """Sale reports for Italian localization - DDT & Fattura accompagnatoria""",
    'author': 'OpenERP Italian Community',
    'website': 'http://www.openerp-italia.org',
    'license': 'AGPL-3',
    "depends" : ['l10n_it_sale', 'report_aeroo_ooo', 'l10n_it_account_report'],
    "init_xml" : [
        ],
    "update_xml" : [
        'reports.xml',
        'wizard/print_fattura_accompagnatoria.xml',
        ],
    "demo_xml" : [],
    "active": False,
    "installable": True
}
