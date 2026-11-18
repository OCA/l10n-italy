# Copyright 2026 Nextev
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "ITA - RiBa Bank Receipts Facility",
    "summary": "Monitor RiBa SBF bank receipts facility per bank:"
    " committed and available at a given date",
    "version": "18.0.1.0.0",
    "category": "Localization/Italy",
    "author": "Nextev, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": ["l10n_it_riba_oca"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_bank_views.xml",
        "views/riba_facility_wizard_views.xml",
    ],
    "installable": True,
}
