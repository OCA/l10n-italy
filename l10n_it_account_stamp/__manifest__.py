# Copyright 2018 Sergio Corato (https://efatto.it)
# Copyright 2018 Enrico Ganzaroli (enrico.gz@gmail.com)
# Copyright 2018 Ermanno Gnan (ermannognan@gmail.com)
# Copyright 2018 Lorenzo Battistini (https://github.com/eLBati)
# Copyright 2018 Sergio Zanchetta (https://github.com/primes2h)
# Copyright 2019 Stefano Consolaro (https://github.com/mymage)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    'name': 'ITA - Imposta di bollo',
    'version': '11.0.1.2.0',
    'category': 'Localization/Italy',
    'summary': 'Gestione automatica dell\'imposta di bollo',
    'author': 'Ermanno Gnan, Sergio Corato, Enrico Ganzaroli, '
              'Agile Business Group, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy',
    'license': 'LGPL-3',
    'depends': [
        'product',
        'account_invoicing',
    ],
    'data': [
        'data/data.xml',
        'views/invoice_view.xml',
        'views/product_view.xml',
        'views/res_config_settings_view.xml',
    ],
    'installable': True,
}
