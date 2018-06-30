# -*- coding: utf-8 -*-
#
##############################################################################
#
#    Author(s): Alessandro Camilli (alessandrocamilli@openforce.it)
#
#    Copyright © 2016 Openforce di Camilli Alessandro (www.openforce.it)
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
#    along with this program. If not, see:
#    http://www.gnu.org/licenses/agpl-3.0.txt.
#
##############################################################################

{
    'name': 'Fleet Fringe Benefit',
    'version': '1.0',
    'category': 'Fleet',
    'description': """
                   Import ACI Tables for Fringe Benefit.
                   The Tables can be dowloaded previous registration from:
                   http://www.aci.it/area-riservata/fringe-benefit.html
                   """,
    'author': "Openforce di Alessandro Camilli,"
            " Odoo Community Association (OCA)",
    'website': 'http://www.openforce.it',
    'license': 'AGPL-3',
    "depends": ['fleet'],
    "data": [
        'views/fleet_view.xml',
        'wizard/import_aci_table_view.xml',
        'security/ir.model.access.csv',
        'data/precision.xml',
    ],
    "installable": True
}
