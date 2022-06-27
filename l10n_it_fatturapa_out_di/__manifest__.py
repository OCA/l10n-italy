# Copyright 2021 Marco Colombo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "ITA - Fattura elettronica - Emissione - Dichiarazione d'intento",
    "version": "14.0.1.0.2",
    "development_status": "Beta",
    "category": "Localization/Italy",
    "summary": "Dichiarazioni d'intento in fatturapa",
    "author": "Marco Colombo," "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_fatturapa_out",
        "l10n_it_declaration_of_intent",
    ],
    "data": [
        "data/invoice_it_template.xml",
    ],
    "installable": True,
    "auto_install": True,
}
