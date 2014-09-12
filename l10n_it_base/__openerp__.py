# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2010-2011 OpenERP Italian Community
#    http://www.openerp-italia.org>
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
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Italian Localisation - Base',
    'version': '0.1',
    'category': 'Localisation/Italy',
    'description': """Italian Localisation module - Base version

Funcionalities:

- Create "Italian Localisation" in the Configuration -> Configuration Menu

""",
    'author': 'OpenERP Italian Community',
    'website': 'http://www.openerp-italia.org',
    'license': 'AGPL-3',
    "depends": ['base'],
    "data": [
        'view/res_config_view.xml',
    ],
    "qweb": [],
    "demo": [],
    "test": [],
    "active": False,
    'installable': True
}
