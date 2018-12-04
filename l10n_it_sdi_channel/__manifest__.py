# -*- coding: utf-8 -*-
# Copyright 2018 Sergio Corato (https://efatto.it)
# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Italian Localization - Fattura Elettronica - Canale SdI',
    "summary": "Aggiunge il canale di invio/ricezione dei file XML "
               "attraverso lo SdI",
    "version": "10.0.1.1.0",
    "development_status": "Alpha",
    "category": "Hidden",
    'website': 'https://github.com/OCA/l10n-italy/tree/10.0/'
               'l10n_it_sdi_channel',
    "author": "Efatto.it di Sergio Corato, Odoo Community Association (OCA)",
    "maintainers": ["sergiocorato"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "account",
        "fetchmail",
        "l10n_it_fatturapa",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/sdi_view.xml",
        "views/company_view.xml",
        'views/fetchmail_server.xml',
        'views/ir_mail_server.xml',
    ],
}
