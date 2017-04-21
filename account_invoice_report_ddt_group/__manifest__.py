# -*- coding: utf-8 -*-
# © 2015 Nicola Malcontenti - Agile Business Group
# © 2016 Andrea Cometa - Apulia Software
# © 2016-2017 Lorenzo Battistini - Agile Business Group
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': "Account invoice report grouped by DDT",
    'version': '10.0.0.1.0',
    'author': 'Agile Business Group, Apulia Software',
    'website': 'http://www.agilebg.com',
    'license': 'LGPL-3',
    'depends': [
        'account', 'l10n_it_ddt',
    ],
    "data": [
        'views/invoice_ddt.xml',
    ],
    "installable": True
}
