# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>). 
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
    'name': "l10n_it_riepilogo_iva_report_qweb",
    'version': '0.1',
    'category': 'report',
    'description': """""",
    'author': 'Andre@ <a.gallina@apuliasoftware.it>',
    'website': '',
    'license': 'AGPL-3',
    "depends": ['report', 'account_vat_period_end_statement' ],
    "data": ['reports.xml',
             'views/vat_period_end_statement.xml',],
    "active": False,
    "installable": True
}
