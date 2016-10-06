# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Associazione Odoo Italia
#    http://www.odoo-italia.org>
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
    'name': 'Account Invoice entry Date',
    'version': '8.0.0.1.0',
    'category': 'Generic Modules/Accounting',
    'description': """This module allows to specify the date to be used by the
move created while confirming (supplier) invoice""",
    'author': "Odoo Italian Community,Odoo Community Association (OCA)",
    'website': 'http://www.odoo-italia.org',
    'license': 'AGPL-3',
    'depends': ['account'],
    'data': ['views/account_view.xml'],
    'active': False,
    'installable': False
}
