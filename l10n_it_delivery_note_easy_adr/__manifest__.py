# Copyright 2022 Bloomup srl
# (https://www.bloomup.it/)
# @author: Matteo Piciucchi <matteo.piciucchi@bloomup.it>
# @author: Letizia Freda <letizia.freda@bloomup.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "ITA - Gestione ADR Semplificata",
    "summary": "Gestione ADR semplificata con calcolo massa virtuale",
    "author": "Odoo Italia Network, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "maintainers": ["Matteo Piciucchi, Letizia Freda, Emily Manfredi, Daniele La Martina"],
    "version": "14.0.1.0.0",
    "category": "Localization/Italy",
    "license": "AGPL-3",
    "depends": [
        "base",
        "stock",
        "l10n_it_delivery_note",
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/config.xml',
        'views/adr.xml',
        'views/product.xml',
        'views/ddt.xml'
    ],
}
