# Copyright 2019-2023 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "ITA - Gestione cespiti - Importazione storico",
    "version": "16.0.1.0.0",
    "category": "Accounting",
    "summary": "Cespiti: importazione storico dati",
    "author": "Openforce, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "external_dependencies": {
        "python": [
            "xlrd",  # Already in Odoo requirements, but let's be sure
            "xlsxwriter",
        ],
    },
    "depends": [
        "l10n_it_asset_management",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/asset.xml",
        "views/asset_category.xml",
        "views/asset_depreciation_mode.xml",
        "views/asset_depreciation_type.xml",
        "wizards/asset_history_import.xml",
    ],
    "installable": True,
    "post_init_hook": "set_import_codes",
}
