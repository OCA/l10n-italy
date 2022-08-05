# Copyright 2019 Simone Rubino
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Italian Localization - Ricevute e fatturazione elettronica",
    "summary": "Modulo per integrare ricevute e fatturazione elettronica",
    "version": "12.0.1.0.1",
    "category": "Localization/Italy",
    "website": "https://github.com/OCA/l10n-italy"
               "/tree/12.0/l10n_it_corrispettivi_fatturapa_out",
    "author": "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_corrispettivi",
        "l10n_it_fatturapa_out"
    ],
    "data": [
        "views/account_invoice_view.xml"
    ],
    "auto_install": True
}
