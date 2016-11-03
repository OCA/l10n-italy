# -*- coding: utf-8 -*-
# © 2015 Nicola Malcontenti - Agile Business Group
# © 2016 Andrea Cometa - Apulia Software
# © 2016 Lorenzo Battistini - Agile Business Group
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': "Account invoice report grouped by DDT",
    'version': '9.0.1.0.0',
    'description': """
This module sets invoice line origin as ddt name.
""",
    'author': 'Agile Business Group, Apulia Software',
    'website': 'http://www.agilebg.com',
    'license': 'GPL-3',
    'depends': [
        'account', 'sale_layout', 'stock_picking_invoice_link', 'l10n_it_ddt',
    ],
    "data": [
        'views/invoice_ddt.xml',
    ],
    "installable": True
}
