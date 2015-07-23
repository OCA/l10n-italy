# -*- coding: utf-8 -*-
##############################################################################
#    
#    Author: Alessandro Camilli per Apulia Software srl
#    Copyright (C) 2015
#    info@apuliasoftware.it - www.apuliasoftware.it
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
    'name': 'Account - Intrastat',
    'version': '0.1',
    'category': 'Account',
    'description': """
    Taxation and customs European Union statements.
    """,
    'author': 'Alessandro Camilli per Apulia Software srl',
    'website': 'http://www.apuliasoftware.it',
    'license': 'AGPL-3',
    "depends": [
        'account',
        'product',
        'stock',
        'report_intrastat'],
    "data": [
        #'data/account.intrastat.transation.nature.csv',
        #'data/account.intrastat.transport.csv',
        #'data/account.intrastat.custom.csv',
        #'data/report.intrastat.code.csv',
        'security/ir.model.access.csv',
        'views/statement.xml',
        'views/product.xml',
        'views/account.xml',
        'views/config.xml',
        ],
    "demo": [],
    "active": False,
    "installable": True
}

