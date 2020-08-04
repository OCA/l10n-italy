# Copyright 2017 Alessandro Camilli - Openforce
# Copyright 2017-2019 Lorenzo Battistini
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    'name': 'ITA - Comunicazione liquidazione IVA',
    'summary': 'Comunicazione liquidazione IVA ed esportazione file xml'
               'conforme alle specifiche dell\'Agenzia delle Entrate',
    'version': '12.0.1.5.4',
    'category': 'Account',
    'author': "Openforce di Camilli Alessandro, "
              "Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/l10n-italy',
    'license': 'LGPL-3',
    'depends': [
        'account_vat_period_end_statement',
        'l10n_it_codici_carica', 'l10n_it_fiscalcode'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/comunicazione_liquidazione.xml',
        'views/config.xml',
        'views/account.xml',
        'wizard/export_file_view.xml',
        'security/security.xml',
    ],
    'installable': True,
}
