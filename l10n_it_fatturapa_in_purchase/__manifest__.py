# Copyright 2018 Lorenzo Battistini
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# Copyright 2019 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    "name": "ITA - Fattura elettronica - Integrazione acquisti",
    "summary": "Modulo ponte tra ricezione fatture elettroniche e acquisti",
    "version": "14.0.1.0.0",
    "category": "Hidden",
    "author": "Agile Business Group, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_fatturapa_in",
        "purchase",
    ],
    "data": [
        "views/invoice_view.xml",
    ],
    "installable": True,
    "auto_install": True,
}
