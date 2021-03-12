# Copyright 2021 Sergio Corato (https://efatto.it)
# Copyright 2021 Matteo Boscolo (https://www.omniasolutions.eu)
# Copyright 2021 Gianmarco Conte <gconte@dinamicheaziendali.it>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Italian Localization - Fattura elettronica - Import ZIP",
    "summary": "Permette di importare uno ZIP con diversi file XML di "
    "fatture elettroniche di acquisto",
    "version": "14.0.1.0.0",
    "category": "other",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Matteo Boscolo, Sergio Corato, Odoo Community Association (OCA)",
    "maintainers": ["info@omniasolutions.eu"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "l10n_it_fatturapa_in",
    ],
    "external_dependencies": {
        "python": ["zipfile"],
    },
    "data": [
        "security/ir.model.access.csv",
        "wizard/wizard_import_invoice.xml",
    ],
}
