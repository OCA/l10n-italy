# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
    "name": "RiBa Issue",
    "version": "0.1",
    "author": "OpenERP Italian Community",
    "category": "Localisation/Italy",
    "website": "http://www.openerp-italia.org",
    "description": """Module to manage RiBa issue.
=================================

This module provides :
----------------------
* a more efficient way to manage RiBa issue.
* a basic mechanism to easily plug various automated issue.
    """,
    'images': ['images/riba_mode.jpeg','images/riba_issue.jpeg'],
    'depends': ['account','account_voucher'],
    'init_xml': [],
    'update_xml': ['wizard/riba_issue_pay_view.xml',
                   'wizard/riba_issue_populate_statement_view.xml',
                   'wizard/riba_issue_order_view.xml',
                   'account_invoice_view.xml',
                   'riba_issue_view.xml',
                   'account_riba_report.xml',
                   ],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
