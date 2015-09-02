# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011-2013 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
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
    'name': 'Italian Localisation - Prima Nota Cassa',
    'version': '0.1',
    'category': 'Localisation/Italy',
    'description': """Accounting reports - Prima Nota Cassa""",
    'author': "OpenERP Italian Community,Odoo Community Association (OCA)",
    'website': 'http://www.openerp-italia.org',
    'license': 'AGPL-3',
    "depends": [
        'account',
        'report'
    ],
    "data": [
        'reports.xml',
        'views/prima_nota_cassa.xml',
        'wizard/wizard_print_prima_nota_cassa.xml',
    ],
    "active": False,
    'installable': True
}
