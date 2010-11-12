# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 Italian OpenERP Community (<http://www.openerp-italia.com>)                            
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
    "name" : "Italy - Generic Chart of Accounts",
    "version" : "0.1",
    "depends" : ['l10n_it',],
    "author" : "OpenERP Italian Community",
    "description": """
    Riclassificazione IV normativa UE per un piano dei conti italiano di un'impresa generica (compreso in l10n_it)
    """,
    "license": "AGPL-3",
    "category" : "Localisation",
    'website': 'http://www.openerp-italia.org/',
    'init_xml': [
        ],
    'update_xml': [
        'data/account.account.type.csv',
        'data/account.account.csv',
        'account_view.xml',
        ],
    'demo_xml': [
        ],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
