# Copyright 2018 Sergio Corato (https://efatto.it)
# Copyright 2018 Enrico Ganzaroli (enrico.gz@gmail.com)
# Copyright 2018 Ermanno Gnan (ermannognan@gmail.com)
# Copyright 2018 Lorenzo Battistini (https://github.com/eLBati)
# Copyright 2018-2020 Sergio Zanchetta (https://github.com/primes2h)
# Copyright 2021 Gianmarco Conte <gconte@dinamicheaziendali.it>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "ITA - Imposta di bollo",
    "version": "14.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Gestione automatica dell'imposta di bollo",
    "author": "Ermanno Gnan, Sergio Corato, Enrico Ganzaroli, "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "LGPL-3",
    "depends": [
        "product",
        "account",
    ],
    "data": [
        "data/data.xml",
        "views/account_move_view.xml",
        "views/product_view.xml",
        "views/company_view.xml",
    ],
    "installable": True,
}
