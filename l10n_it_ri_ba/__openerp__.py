# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#    All Rights Reserved 
#    Thanks to Cecchi s.r.l http://www.cecchi.com/
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
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
    "name": "RiBa Issue",
    "version": "1.0",
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
    'images': [],
    'depends': ['account','account_voucher', 'l10n_it_account'],
    'init_xml': [],
    'update_xml': [
                   'security/riba_issue_security.xml',
                   'security/ir.model.access.csv',
                   'wizard/riba_issue_pay_view.xml',
                   'wizard/riba_issue_order_view.xml',
                   'wizard/riba_file_export.xml',
                   'account_invoice_view.xml',
                   'riba_issue_view.xml',
                   'riba_report.xml',
                   'riba_sequence.xml',
                   'account_riba_workflow.xml'
                   ],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
