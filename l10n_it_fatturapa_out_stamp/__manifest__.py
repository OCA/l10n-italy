# Copyright 2018 Lorenzo Battistini
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Italian Localization - Fattura elettronica - Integrazione bollo",
    "summary": "Modulo ponte tra emissione fatture elettroniche e imposta di "
               "bollo",
    "version": "12.0.2.0.0",
    "development_status": "Beta",
    "category": "Hidden",
    "website": "https://github.com/OCA/l10n-italy"
               "/tree/12.0/l10n_it_fatturapa_out_stamp",
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    "maintainers": ["eLBati"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "l10n_it_fatturapa_out",
        "l10n_it_account_stamp",
    ],
    "data": [
    ],
}
