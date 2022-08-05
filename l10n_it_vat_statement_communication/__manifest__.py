# Copyright 2017 Alessandro Camilli - Openforce
# Copyright 2017-2019 Lorenzo Battistini
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'ITA - Comunicazione liquidazione IVA',
    'summary': 'Comunicazione liquidazione IVA ed esportazione file xml'
               'conforme alle specifiche dell\'Agenzia delle Entrate',
    'version': '12.0.1.6.1',
    'category': 'Account',
    'author': "Openforce di Camilli Alessandro, "
              "Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/l10n_it_vat_statement_communication',
    'license': 'AGPL-3',
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
