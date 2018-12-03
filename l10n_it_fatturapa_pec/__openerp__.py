# -*- coding: utf-8 -*-
# Author(s): Andrea Colangelo (andreacolangelo@openforce.it)
# Copyright 2018 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2018 Sergio Corato (https://efatto.it)
# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Italian Localization - FatturaPA - Emission - PEC Support',
    'version': '8.0.1.1.0',
    'category': 'Localization/Italy',
    'summary': 'Send electronic invoices via PEC',
    'author': 'Openforce Srls Unipersonale, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy',
    'license': 'LGPL-3',
    'depends': [
        'fetchmail',
        'l10n_it_fatturapa_out',
        # 'l10n_it_fatturapa_in', Enable this dep as soon as
        # the module is ready
        'l10n_it_sdi_channel',
    ],
    'data': [
        'views/account.xml',
        'views/fatturapa_attachment_out.xml',
        'wizard/send_pec_view.xml',
    ],
    'installable': True
}
