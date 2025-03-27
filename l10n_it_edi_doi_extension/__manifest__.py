# Copyright 2025 Nextev Srl
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Declaration of Intent for Italy (OCA)",
    "version": "18.0.1.0.0",
    "author": "Nextev Srl, " "Odoo Community Association (OCA)",
    "category": "Accounting",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": ["l10n_it_edi_doi", "purchase"],
    "data": [
        "views/l10n_it_edi_doi_declaration_of_intent_views.xml",
        "views/res_company.xml",
        "views/purchase_order_views.xml",
        "views/account_move_views.xml",
    ],
    "installable": True,
}
