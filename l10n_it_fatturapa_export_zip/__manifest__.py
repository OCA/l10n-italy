# -*- coding: utf-8 -*-
# Copyright 2019 Sergio Corato (https://efatto.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Export fatturapa xml zip file",
    "summary": "Add ability to export multiple xml of e-invoice in "
               "a zip file.",
    "version": "10.0.1.0.0",
    "development_status": "Alpha",
    "category": "other",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Efatto.it di Sergio Corato, Odoo Community Association (OCA)",
    "maintainers": ["sergiocorato"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "l10n_it_fatturapa_out",
        "l10n_it_fatturapa_in",
    ],
    "data": [
        "views/wizard.xml",
        "views/attachment_view.xml",
    ],
}
