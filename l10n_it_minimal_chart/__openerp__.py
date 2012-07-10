# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-2012
#    Associazione OpenERP Italia (<http://www.openerp-italia.org>)
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
    "name" : "Italy - Minimal Chart of Accounts",
    "version" : "0.1",
    "depends" : ['l10n_it'],
    "author" : "OpenERP Italian Community",
    "description": """
    Piano dei conti italiano minimale. Contiene solo i conti strettamente necessari a configurare una contabilità di base funzionante in OpenERP. Il modulo va inteso come una base di partenza per costruire il proprio piano dei conti.
    """,
    "license": "AGPL-3",
    "category" : "Localization/Account Charts",
    'website': 'http://www.openerp-italia.org/',
    'init_xml': [
        ],
    'update_xml': [
        'data/account.account.template.csv',
        ],
    'demo_xml': [
        ],
    'installable': True,
    'active': False,
}
