# Copyright 2018 Lorenzo Battistini
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "ITA - Fattura elettronica - Integrazione bollo",
    "summary": "Modulo ponte tra emissione fatture elettroniche e imposta di bollo",
    "version": "14.0.1.0.0",
    "development_status": "Beta",
    "category": "Localization/Italy",
    "website": "https://github.com/OCA/l10n-italy",
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
    "data": ["views/account_invoice_it_dati_bollo.xml"],
}
