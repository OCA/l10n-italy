# -*- encoding: utf-8 -*-
#
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 Italian OpenERP Community
#    (<http://www.openerp-italia.com>)
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
#

{
    "name": "Italy - 4th EU Directive - Consolidation Chart of Accounts",
    "version": "0.1",
    "depends": ['account_chart', ],
    "author": "OpenERP Italian Community,Odoo Community Association (OCA)",
    "description": """
    Riclassificazione IV direttiva UE per un piano dei conti italiano di
    un'impresa generica
    I nuovi conti inseriti non hanno relazioni con altri conti precedentemente
    esistenti
    Le eventuali relazioni debbono essere inserite manualmente
    """,
    "license": "AGPL-3",
    "category": "Localisation/Italy",
    'website': 'http://www.openerp-italia.org/',
    'data': [
        'data/account.account.type.csv',
        'data/account.account.csv',
        'account_view.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'active': False,
}
