# Author(s): Andrea Colangelo (andreacolangelo@openforce.it)
# Copyright 2018 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2018-2019 Sergio Corato (https://efatto.it)
# Copyright 2018-2019 Lorenzo Battistini <https://github.com/eLBati>
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# Copyright 2019 Roberto Fichera (https://levelprime.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'ITA - Fattura elettronica - Supporto PEC',
    'version': '12.0.2.1.0',
    'category': 'Localization/Italy',
    'summary': 'Invio fatture elettroniche tramite PEC',
    'author': 'Openforce Srls Unipersonale, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/l10n_it_fatturapa_pec',
    'license': 'AGPL-3',
    'depends': [
        'fetchmail',
        'l10n_it_fatturapa_out',
        'l10n_it_fatturapa_in',
        'l10n_it_sdi_channel',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/fatturapa_attachment_out.xml',
        'views/fetchmail_view.xml',
        'views/company_view.xml',
        'views/sdi_view.xml',
        'views/ir_mail_server.xml',
        'data/fetchmail_data.xml',
        'data/config_parameter.xml',
        'data/sdi_channel_demo.xml',
    ],
    'installable': True,
}
