# Copyright 2014 Davide Corio
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# Copyright 2018 Sergio Corato
# Copyright 2020 Matteo Mircoli Openforce srls
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'ITA - Fattura elettronica - Emissione',
    'version': '12.0.3.1.2',
    'development_status': 'Beta',
    'category': 'Localization/Italy',
    'summary': 'Emissione fatture elettroniche',
    'author': 'Davide Corio, Agile Business Group, Innoviu,'
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/l10n_it_fatturapa_out',
    'license': 'AGPL-3',
    'depends': [
        'l10n_it_account',
        'l10n_it_fatturapa',
        'l10n_it_split_payment',
        ],
    'data': [
        'security/res_groups.xml',
        'wizard/wizard_export_fatturapa_view.xml',
        'wizard/wizard_export_fatturapa_view_regenerate.xml',
        'views/attachment_view.xml',
        'views/account_view.xml',
        'views/partner_view.xml',
        'views/company_view.xml',
        'security/ir.model.access.csv',
        'data/l10n_it_fatturapa_out_data.xml',
        'security/rules.xml',
    ],
    'installable': True,
    'external_dependencies': {
        'python': [
            'unidecode',
            'pyxb',  # pyxb 1.2.6
        ],
    }
}
