# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Associazione Odoo Italia
#    (<http://www.odoo-italia.org>).
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
##############################################################################
{
    'name': 'Italian Localisation - Fiscal Code',
    'version': '8.0.0.1.2',
    'category': 'Localisation/Italy',
    'description': """
This module customizes Odoo in order to fit italian laws and mores

Functionalities:

- Fiscal code computation for partner

External depends:

    * Python codicefiscale https://pypi.python.org/pypi/codicefiscale

""",
    'author': "Odoo Italian Community,Odoo Community Association (OCA)",
    'website': 'http://www.odoo-italia.org',
    'license': 'AGPL-3',
    'depends': ['base_vat'],
    'external_dependencies': {
        'python': ['codicefiscale'],
    },
    'data': [
        'view/fiscalcode_view.xml',
        'wizard/compute_fc_view.xml',
        'data/res.city.it.code.csv',
        "security/ir.model.access.csv"
        ],
    'qweb': [],
    'demo': [],
    'test': [
        'test/fiscalcode.yml',
        ],
    'active': False,
    'installable': True
}
