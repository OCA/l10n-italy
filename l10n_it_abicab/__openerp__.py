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
Adds to res.bank the ABI/CAB data (bank identification numbers).


Contributors
------------

Franco Tampieri <franco@tampieri.info>
Alessandro Camilli <a.camilli@yahoo.it>
Lorenzo Battistini <lorenzo.battistini@agilebg.com>
""",
    'author': "OpenERP Italian Community,Odoo Community Association (OCA)",
    'license': 'AGPL-3',
    'depends': ['base', 'account'],
    'test': [
        'test/abicab.yml',
    ],
    'website': 'http://www.openerp-italia.org/',
    'data': ['abicab_view.xml'],
    'installable': True,
}
