# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Lorenzo Battistini (<lorenzo.battistini@agilebg.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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
    'name': "Italian toponyms - Provinces",
    'version': '0.2',
    'category': 'Localisation/Italy',
    'description': """
Italian provinces
-----------------

This module adds the basic structure to partners in order to handle Italian
provinces.
It depends on base_location and extends it to automate address compilation.
""",
    'author': 'Agile Business Group',
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    "depends" : ['base_location'],
    "data" : [
        'better_zip_view.xml',
        'partner_view.xml',
        'province_view.xml',
        ],
    'test': [
        ],
    "demo" : [
        ],
    "active": False,
    "installable": True
}
