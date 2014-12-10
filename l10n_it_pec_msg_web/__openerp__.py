# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Innoviu srl (<http://www.innoviu.it>).
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
    'name': 'Pec Mail Widget',
    'description': '''
This module add Pec in widget mail

This module is compatible with OpenERP 7.0.
''',
    "version": "1.0",
    "author": "Odoo Italian Community",
    "category": "Certified Mailing",
    "website": "http://www.odoo-italia.org",
    'license': 'AGPL-3',
    'depends': [
        'web',
        ],
    'js': [
           'static/src/js/pec_widget.js',
        ],
    'installable': True,
    'auto_install': False,
}
