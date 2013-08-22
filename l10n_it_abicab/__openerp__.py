# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012
#    Associazione OpenERP Italia (<http://www.openerp-italia.org>)
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
#############################################################################

{
    'name': 'Italian Localisation - Base Bank ABI/CAB codes',
    'version': '1.0',
    'category': 'Localisation/Italy',
    'description': """
    Insert in the res.bank model the proprieties of the ABI/CAB
    Utility to import italian bank from txt file 
    """,
    'author': 'OpenERP Italian Community',
    'depends': ['base'],
    'website': 'http://www.openerp-italia.org/',
    'update_xml': ['abicab_view.xml'],
    'installable': True,
    'active': False,
    'certificate': '',
}