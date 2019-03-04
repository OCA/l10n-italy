# -*- coding: utf-8 -*-
##############################################################################
#
#    Italian Localization - FatturaPA - Emission - PEC Support
#
#    Author(s): Andrea Colangelo (andreacolangelo@openforce.it)
#    Copyright © 2018 Openforce Srls Unipersonale (www.openforce.it)
#    Copyright © 2018 Sergio Corato (https://efatto.it)
#    Copyright © 2018 Lorenzo Battistini (https://github.com/eLBati)
#    Copyright © 2018 Enrico Ganzaroli (enrico.gz@gmail.com)
#    Copyright © 2018 Ermanno Gnan (ermannognan@gmail.it)
#    Copyright © 2018 Daniel Smerghetto (daniel.smerghetto@omniasolutions.eu)
#
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
##############################################################################
{
    'name': 'Italian Localization - FatturaPA - Emission - PEC Support',
    'version': '7.0.1.2.0',
    'category': 'Localization/Italy',
    'summary': 'Send electronic invoices via PEC',
    'author': 'Openforce Srls Unipersonale, Odoo Community Association (OCA)',
    'description': """
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License


Italian Localization - FatturaPA - Emission - PEC Support
=========================================================
This module allows you to send and receive electronic invoice XML file version
1.2 http://www.fatturapa.gov.it/export/fatturazione/en/sdi.htm
via PEC

Notifications from SDI are parsed and transmission state is tracked.

USAGE
=====

* In electronic invoice out attachment you can click "Send Via PEC" button.

* Supplier electronic invoices are automatically created, fetched from PEC
mailbox.
    """,

    'website': 'https://github.com/OCA/l10n-italy',
    'license': 'AGPL-3',
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
        'views/mail_message_view.xml',
    ],
    'installable': True
}
