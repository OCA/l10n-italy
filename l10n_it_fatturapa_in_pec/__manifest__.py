# -*- coding: utf-8 -*-
# Copyright 2018 Sergio Corato (https://efatto.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "FatturaPA and B2B receive from pec",
    "summary": "Receive xml invoices in pec mail from SdI.",
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
        "account",
        "mail",
        "l10n_it_fatturapa_in",
        "l10n_it_fatturapa_out_pec",
    ],
    "data": [
    ],
}
