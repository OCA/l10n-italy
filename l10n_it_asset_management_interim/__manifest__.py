# Copyright 2026 Luca Orioli <lucaorioli@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "ITA - Gestione Cespiti - Ammortamenti infrannuali",
    "version": "18.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Interim depreciation entries, reversed, without depreciation lines",
    "author": "Luca Orioli, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_asset_management",
    ],
    "data": [
        "wizard/asset_generate_depreciation_view.xml",
        "wizard/asset_previsional_report_view.xml",
    ],
    "development_status": "Beta",
}
