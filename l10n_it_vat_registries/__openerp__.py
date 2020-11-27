# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2011-2013 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    Copyright (C) 2012-2015 Agile Business Group sagl
#    Copyright (C) 2012-15 LinkIt Spa (<http://http://www.linkgroup.it>)
#    (<http://www.agilebg.com>)
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
#
{
    'name': 'Italian Localization - VAT Registries',
    'version': '8.0.3.0.0',
    'category': 'Localization/Italy',
    "author": "Agile Business Group, Odoo Community Association (OCA)"
              ", LinkIt Spa",
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    "depends": [
        'account',
        'l10n_it_account'
        ],
    "data": [
        'reports.xml',
        'wizard/print_registro_iva.xml',
        'account_view.xml',
        'views/report_registro_iva.xml',
        'security/ir.model.access.csv',
        'security/vat_registry_security.xml',
        'account_journal_view.xml',
        'account_tax_registry_view.xml',
    ],
    "installable": True,
}
