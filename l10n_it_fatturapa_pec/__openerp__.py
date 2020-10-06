# -*- coding: utf-8 -*-
# Author(s): Andrea Colangelo (andreacolangelo@openforce.it)
# Copyright 2018 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2018-2019 Sergio Corato (https://efatto.it)
# Copyright 2018-2019 Lorenzo Battistini <https://github.com/eLBati>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Italian Localization - Fattura elettronica - Supporto PEC',
    'version': '8.0.1.5.0',
    'category': 'Localization/Italy',
    'summary': 'Send electronic invoices via PEC',
    'author': 'Openforce Srls Unipersonale, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy',
    'license': 'AGPL-3',
    'depends': [
        'fetchmail',
        'l10n_it_fatturapa_out',
        'l10n_it_fatturapa_in',
        'l10n_it_sdi_channel',
    ],
    'data': [
        'security/groups.xml',
        'views/account.xml',
        'views/fatturapa_attachment_out.xml',
        'wizard/send_pec_view.xml',
        'views/fetchmail_view.xml',
        'security/ir.model.access.csv',
        'views/company_view.xml',
        'data/fetchmail_data.xml',
    ],
    'installable': True
}
