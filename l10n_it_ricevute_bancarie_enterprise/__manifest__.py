# Copyright 2020 Ilaria Franchini <i.franchini@apuliasoftware.it>
# Copyright 2021 Matteo Boscolo <matteo.boscolo@omniasolutions.eu>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Fix l10n_it_ricevute_bancarie for enterprise",
    "version": "14.0.1.0.0",
    "author": "Apulia software, Odoo Community Association (OCA)",
    "category": "Localization/Italy",
    "summary": "Fix l10n_it_ricevute_bancarie for enterprise",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": ["account_accountant", "l10n_it_ricevute_bancarie"],
    "data": ["views/riba_view.xml"],
    "installable": True,
}
