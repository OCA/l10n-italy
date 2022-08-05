#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'ITA - Fattura elettronica - Supporto SDICoop',
    'version': '12.0.2.2.0',
    'category': 'Localization/Italy',
    'summary': 'Invio fatture elettroniche tramite SDICoop',
    'author': 'TAKOBI, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/l10n_it_fatturapa_sdicoop',
    'license': 'AGPL-3',
    'depends': [
        'l10n_it_fatturapa_out',
        'l10n_it_fatturapa_in',
        'l10n_it_sdi_channel',
    ],
    'data': [
        'data/sdi_channel_data.xml',
    ],
}
