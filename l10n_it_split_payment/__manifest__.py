# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Abstract (http://www.abstract.it)
#    Author: Davide Corio <davide.corio@abstract.it>
#    Copyright 2015 Lorenzo Battistini - Agile Business Group
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
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
    'name': 'Split Payment',
    'version': '8.0.1.0.0',
    'category': 'Localization/Italy',
    'summary': 'Split Payment',
    'author': 'Abstract, Odoo Community Association (OCA)',
    'website': 'http://www.abstract.it',
    'license': 'AGPL-3',
    'depends': [
        'account'],
    'data': [
        'views/account_view.xml',
        'views/config_view.xml',
    ],
    'installable': False,
}
