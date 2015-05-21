# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Abstract (http://www.abstract.it)
#    @author Davide Corio <davide.corio@abstract.it>
#    Copyright (C) 2014 Agile Business Group (http://www.agilebg.com)
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
    'name': 'DDT',
    'version': '1.0',
    'category': 'Localization/Italy',
    'summary': 'Documento di Trasporto',
    'author': 'Davide Corio, Odoo Community Association (OCA), '
              'Agile Business Group',
    'website': 'http://www.odoo-italia.org/',
    'depends': ['sale_stock', 'stock_account'],
    'data': [
        'security/ir.model.access.csv',
        'data/stock_data.xml',
        'views/account_view.xml',
        'views/partner_view.xml',
        'views/sale_view.xml',
        'views/stock_view.xml',
        'wizard/ddt_from_pickings_view.xml',
        'wizard/ddt_create_invoice_view.xml',
        'wizard/add_picking_to_ddt.xml',
        'workflow/stock_ddt_workflow.xml',
        'views/report_ddt.xml'
    ],
    'test': ['tests/new_ddt.yml'],
    'installable': True,
}
