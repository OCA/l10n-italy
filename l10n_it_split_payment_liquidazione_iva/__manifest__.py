# -*- coding: utf-8 -*-
#
##############################################################################
#
#    Author(s): Silvio Gregorini (silviogregorini@openforce.it)
#
#    Copyright © 2018 Openforce Srls Unipersonale (www.openforce.it)
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
#    along with this program. If not, see:
#    http://www.gnu.org/licenses/agpl-3.0.txt.
#
##############################################################################

{
    'name': 'Split Payment - Liquidazione IVA',
    'version': '11.0.1.0.0',
    'category': 'Accounting & Finance',
    'description': """
            Improvements to end period VAT statements through implementation of split payments
                   """,
    'author': 'Openforce Srls Unipersonale',
    'website': 'http://www.openforce.it',
    'license': 'AGPL-3',
    "depends": ['account_vat_period_end_statement', 'l10n_it_split_payment'],
    "data": [
        'views/account_config_view.xml',
    ],
    "active": False,
    "installable": True
}
