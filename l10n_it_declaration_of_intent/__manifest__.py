# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>,
# Copyright 2019 Alessandro Camilli <alessandrocamilli@openforce.it>,
# Link IT <info@linkgroup.it>
# Copyright 2022 Alex Comba <alex.comba@agilebg.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "ITA - Dichiarazione di intento",
    "summary": "Gestione dichiarazioni di intento",
    "version": "16.0.1.1.0",
    "license": "AGPL-3",
    "author": "Francesco Apruzzese, Sergio Corato, Glauco Prina, Lara Baggio, "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "depends": [
        "account",
        "sale",
    ],
    "data": [
        "security/declaration_security.xml",
        "security/ir.model.access.csv",
        "data/sequence.xml",
        "wizard/select_declarations_view.xml",
        "views/account_view.xml",
        "views/declaration_of_intent_view.xml",
        "views/company_view.xml",
        "views/account_invoice_view.xml",
    ],
    "demo": [
        "demo/declaration_of_intent.xml",
    ],
}
