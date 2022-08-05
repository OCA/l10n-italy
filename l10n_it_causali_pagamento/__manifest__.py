# Copyright 2018 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Italian Localization - Causali pagamento',
    'summary':
        'Aggiunge la tabella delle causali di pagamento da usare ad esempio '
        'nelle ritenute d\'acconto',
    'version': '12.0.2.0.0',
    "development_status": "Production/Stable",
    'category': 'Account',
    'author': "Agile Business Group,"
        "Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/l10n_it_causali_pagamento',
    'license': 'AGPL-3',
    'depends': [
        'l10n_it_account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/causali_pagamento_data.xml',
        'views/causali_pagamento_view.xml',
    ],
    'installable': True,
}
