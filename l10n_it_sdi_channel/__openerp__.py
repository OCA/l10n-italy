# -*- coding: utf-8 -*-
# Copyright 2018 Sergio Corato (https://efatto.it)
# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "SdI channel",
    "summary": "Add channel to send-receice xml files to SdI.",
    "version": "8.0.1.0.0",
    "development_status": "Alpha",
    "category": "Hidden",
    "website": "https://github.com/OCA/l10n-italy",
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
