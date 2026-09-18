# Copyright 2025 Nextev Srl
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Declaration of Intent for Italy (OCA)",
    "version": "18.0.1.1.2",
    "author": "Nextev Srl, " "Odoo Community Association (OCA)",
    "category": "Accounting",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": ["l10n_it_edi_doi", "purchase"],
    "data": [
        "data/sequence.xml",
        "security/ir.model.access.csv",
        "views/l10n_it_edi_doi_declaration_of_intent_views.xml",
        "views/res_company.xml",
        "views/purchase_order_views.xml",
        "views/account_move_views.xml",
        "views/plafond_year_views.xml",
    ],
    "installable": True,
    "pre_init_hook": "_l10n_it_edi_doi_extension_pre_init_hook",
    "post_init_hook": "_l10n_it_edi_doi_extension_post_init_hook",
    "external_dependencies": {
        "python": [
            "openupgradelib",
        ],
    },
}
