# -*- coding: utf-8 -*-
# Author(s): Andrea Colangelo (andreacolangelo@openforce.it)
# Copyright 2018 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2018-2019 Sergio Corato (https://efatto.it)
# Copyright 2018-2019 Lorenzo Battistini <https://github.com/eLBati>
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# Copyright 2019 Roberto Fichera (https://levelprime.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    'name': 'Italian Localization - Fattura elettronica - Supporto PEC',
    'version': '10.0.1.9.1',
    'category': 'Localization/Italy',
    'summary': 'Invio fatture elettroniche tramite PEC',
    'author': 'Openforce Srls Unipersonale, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy'
               'l10n_it_fatturapa_pec',
    'license': 'LGPL-3',
    'depends': [
        'fetchmail',
        'l10n_it_fatturapa_out',
        'l10n_it_fatturapa_in',
        'l10n_it_sdi_channel',
    ],
    'data': [
        'security/groups.xml',
        'views/fatturapa_attachment_out.xml',
        'wizard/send_pec_view.xml',
        'wizard/wizard_export_fatturapa_view.xml',
        'views/account.xml',
        'views/fetchmail_view.xml',
        'security/ir.model.access.csv',
        'views/company_view.xml',
        'data/fetchmail_data.xml',
    ],
    'installable': True
}
