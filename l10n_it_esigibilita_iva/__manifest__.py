# Copyright 2017 Alessandro Camilli - Openforce
# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': "Italian Localization - Esigibilita' IVA",
    'version': '12.0.2.0.0',
    'development_status': 'Beta',
    'category': 'Account',
    'author': "Openforce di Camilli Alessandro, "
              "Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/l10n_it_esigibilita_iva',
    'license': 'LGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'views/account_view.xml',
    ],
    'installable': True,
}
