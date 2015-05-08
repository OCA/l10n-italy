# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2013
#    Associazione OpenERP Italia (<http://www.openerp-italia.org>)
#
#    Copyright (c) 2013 Agile Business Group (http://www.agilebg.com)
#    @author Lorenzo Battistini
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
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
#

{
    'name': 'DDT report using Webkit Library',
    'version': '1.0',
    'category': 'Reports/Webkit',
    'description': """
This module adds the webkit DDT report
    """,
    'author': "Agile Business Group,Odoo Community Association (OCA)",
    'website': 'http://www.agilebg.com',
    'depends': ['report_webkit', 'l10n_it_sale', 'base_headers_webkit'],
    'data': ['report.xml'],
    'installable': True,
    'active': False,
}
