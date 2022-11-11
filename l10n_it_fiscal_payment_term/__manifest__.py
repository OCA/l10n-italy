# Copyright 2014 Davide Corio <davide.corio@abstract.it>
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# Copyright 2019 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# Copyright 2022 Marco Colombo (marco.colombo@phi.technology)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "ITA - Termini fiscali di pagamento",
    "version": "16.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Condizioni di pagamento delle fatture elettroniche",
    "author": "Davide Corio, Agile Business Group, Innoviu, "
    "Odoo Italia Network, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_account",  # for tests only
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/fatturapa_data.xml",
        "views/account_view.xml",
    ],
    "installable": True,
}
