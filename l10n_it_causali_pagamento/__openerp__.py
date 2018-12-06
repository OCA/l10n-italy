# -*- coding: utf-8 -*-
# Copyright 2018 Lorenzo Battistini - Agile Business Group
# Copyright 2018 Gianmarco Conte - Dinamiche Aziendali srl
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Italian Localization - Causali pagamento',
    'summary':
        'Aggiunge la tabella delle causali di pagamento da usare ad esempio '
        'nelle ritenute d\'acconto',
    'version': '8.0.1.0.0',
    'category': 'Account',
    'author': "Agile Business Group,"
        "Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/l10n-italy/',
    'license': 'LGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/causali_pagamento_data.xml',
        'views/causali_pagamento_view.xml',
    ],
    'installable': True,
}
