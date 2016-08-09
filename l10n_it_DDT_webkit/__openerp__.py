# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013
#    Associazione OpenERP Italia (<http://www.openerp-italia.org>)
#
#    Copyright (c) 2013 Agile Business Group (http://www.agilebg.com)
#    @author Lorenzo Battistini
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
    'name': 'DDT report using Webkit Library',
    'version': '1.0',
    'category': 'Reports/Webkit',
    'description': """
This module adds the webkit DDT report
    """,
    'author': "Agile Business Group,Odoo Community Association (OCA)",
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    'depends': ['report_webkit', 'l10n_it_sale', 'base_headers_webkit'],
    'data': ['report.xml'],
    'installable': False,
    'active': False,
}
