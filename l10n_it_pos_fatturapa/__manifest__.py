# Copyright 2019 Roberto Fichera
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "ITA - POS - Fattura elettronica",
    "summary": "Gestione dati fattura elettronica del cliente all'interno "
               "dell'interfaccia del POS",
    "version": "12.0.1.0.2",
    "development_status": "Beta",
    "category": "Point Of Sale",
    "website": "https://github.com/OCA/l10n-italy"
               "/tree/12.0/l10n_it_pos_fatturapa",
    "author": "Roberto Fichera, Odoo Community Association (OCA)",
    "maintainers": ["robyf70"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "pos_partner_firstname",
        "l10n_it_pos_fiscalcode",
        "l10n_it_fatturapa",
    ],
    'qweb': [
        'static/src/xml/pos.xml'
    ],
    'data': [
        'views/assets.xml',
    ],
}
