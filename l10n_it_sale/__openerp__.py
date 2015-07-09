# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2010 Associazione OpenERP Italia
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
#
{
    'name': 'Italian Localisation - Sale',
    'version': '0.2',
    'category': 'Localisation/Italy',
    'description': """OpenERP Italian Localization - Sale version

Functionalities:

- Documento di trasporto

""",
    'author': "OpenERP Italian Community,Odoo Community Association (OCA)",
    'website': 'http://www.openerp-italia.org',
    'license': 'AGPL-3',
    "depends": ['stock', 'sale', 'account', 'delivery'],
    "data": [
        'wizard/assign_ddt.xml',
        'stock/picking_view.xml',
        'stock/carriage_condition_view.xml',
        'stock/transportation_reason_view.xml',
        'stock/goods_description_view.xml',
        'stock/transportation_reason_data.xml',
        'stock/goods_description_data.xml',
        'stock/carriage_condition_data.xml',
        'stock/sequence.xml',
        'sale/sale_view.xml',
        "security/ir.model.access.csv",
        'partner/partner_view.xml',
        'account/invoice_view.xml',
    ],
    "demo": [],
    "active": False,
    "installable": True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
