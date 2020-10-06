# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Abstract srl (<http://www.abstract.it>)
#    Copyright (C) 2015 Agile Business Group (<http://www.agilebg.com>)
#    Copyright (C) 2015 Link It Spa (<http://www.linkgroup.it/>)
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
    'name': 'Italian Localization - Account',
    'version': '8.0.1.1.0',
    'category': 'Hidden',
    'author': "Agile Business Group,Abstract,Odoo Community Association (OCA)",
    'website': 'http://www.odoo-italia.org',
    'license': 'AGPL-3',
    "depends": ['account', 'l10n_it_fiscalcode', 'l10n_it_base'],
    "data": [
        'views/account_view.xml',
        'reports/account_reports_view.xml',
        'views/config_view.xml',
    ],
    'installable': True,
    # this post_init script only works when you install account and
    # l10n_it_account in 2 different instants
    'post_init_hook': 'post_init_hook',
}
