# Copyright 2019 Sergio Corato (https://efatto.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Italian Localization - Fattura elettronica - Export ZIP",
    "summary": "Permette di esportare in uno ZIP diversi file XML di "
               "fatture elettroniche",
    "version": "12.0.1.0.1",
    "development_status": "Beta",
    "category": "other",
    "website": "https://github.com/OCA/l10n-italy"
               "/tree/12.0/l10n_it_fatturapa_export_zip",
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
        "wizard/export_fatturapa_view.xml",
        "views/attachment_view.xml",
    ],
}
