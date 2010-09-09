# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2010 OpenERP Italian Community (<http://www.openerp-italia.org>). 
#    All Rights Reserved
#    $Id$
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
    'name': 'Italian Localisation',
    'version': '1.1',
    'category': 'Localisation/Italy',
    'description': """This module customizes OpenERP in order to fit italian laws and mores""",
    'author': 'OpenERP Italian Community',
    'website': 'http://www.openerp-italia.org',
    "depends" : ['base','account','base_vat','account_chart','base_iban','stock','sale'],
    "init_xml" : [
    ],
    "update_xml" : ['partner/partner_view.xml', 'stock/picking_view.xml', 'stock/carriage_condition_view.xml',
                    'stock/transportation_reason_view.xml', 'stock/goods_description_view.xml', 
                    'stock/transportation_reason_data.xml', 'stock/goods_description_data.xml', 
                    'stock/carriage_condition_data.xml', 'sale/sale_view.xml', "security/ir.model.access.csv",
                    'partner/data/res.province.csv', 'partner/data/res.municipality.csv', 'partner/data/res.region.csv'],
    "demo_xml" : [],
    "active": False,
    "installable": True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

