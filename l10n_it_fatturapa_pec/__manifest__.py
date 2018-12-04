# -*- coding: utf-8 -*-
# Author(s): Andrea Colangelo (andreacolangelo@openforce.it)
# Copyright 2018 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2018 Sergio Corato (https://efatto.it)
# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    'name': 'Italian Localization - Fattura Elettronica - Supporto PEC',
    'version': '10.0.1.2.0',
    'category': 'Localization/Italy',
    'summary': 'Invio fatture elettroniche tramite PEC',
    'author': 'Openforce Srls Unipersonale, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy/tree/10.0/'
               'l10n_it_fatturapa_pec',
    'license': 'LGPL-3',
    'depends': [
        'fetchmail',
        'l10n_it_fatturapa_out',
        'l10n_it_fatturapa_in',
        'l10n_it_sdi_channel',
    ],
    'data': [
        'views/account.xml',
        'views/fatturapa_attachment_out.xml',
        'wizard/send_pec_view.xml',
        'views/fetchmail_view.xml',
    ],
    'installable': True
}
