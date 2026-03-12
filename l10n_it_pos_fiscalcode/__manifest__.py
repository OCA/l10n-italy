# Copyright 2019 Lorenzo Battistini
# Copyright 2026 Simone Rubino
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "ITA - POS - Codice fiscale",
    "summary": "Gestione codice fiscale del cliente all'interno "
    "dell'interfaccia del POS",
    "version": "18.0.1.0.0",
    "development_status": "Beta",
    "category": "Point Of Sale",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Odoo Community Association (OCA)",
    "maintainers": ["eLBati"],
    "license": "AGPL-3",
    "depends": [
        "point_of_sale",
        "l10n_it_edi",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "l10n_it_pos_fiscalcode/static/src/**/*",
        ],
        "web.assets_tests": [
            "l10n_it_pos_fiscalcode/static/tests/tours/**/*",
        ],
    },
}
