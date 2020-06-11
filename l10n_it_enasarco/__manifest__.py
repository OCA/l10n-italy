##############################################################################
#
#    Author(s): Alessandro Camilli (alessandrocamilli@openforce.it)
#
#    Copyright © 2018 Openforce (www.openforce.it)
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
    'name': 'Enasarco',
    'version': '11.0.1.0.1',
    'category': 'Account',
    'description': """
        Manage Enasarco amount in the invoice
        """,
    'author': 'Openforce',
    'website': 'http://www.openforce.it',
    'license': 'AGPL-3',
    "depends": ['account_invoicing', 'l10n_it_withholding_tax'],
    "data": [
        'views/res_config_setting.xml',
        'views/account_invoice_view.xml',
        'views/enasarco.xml',
    ],
    'qweb': [
        "static/src/xml/account_payment.xml",
    ],
    "active": False,
    "installable": True
}
